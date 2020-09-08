# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

import logging
import time
import json
from facerecognition import facenet
import collections
import time
import numpy as np


threshold = 0.3
timeWindowInSecs = 120

class UnKnownFace(object):
    '''
    UnKnownFace will maintain a circular buffer of given size.
    Each slot in the buffer refers to 1 second.
    We will be deleting old messages if it exceeds the time duration(size)
    '''

    def __init__(self,threshold,size):
        self.buffer = collections.deque(maxlen=size)
        self.size = size
        self.threshold = threshold

    def deleteOldRecords(self):
        current_time = int(time.time())
        while len(self.buffer) > 0 :
            unknownface = self.buffer.popleft()
            last_time = unknownface['time']
            # Check if time difference is greater than buffer size
            if current_time -last_time < self.size :
                self.buffer.appendleft(unknownface)
                return
    
    def addUnknownface(self,embedding):
        current_time = int(time.time())
        entry = {}
        entry['embedding'] = embedding
        entry['time'] = current_time
        self.buffer.append(entry)

    def match(self,embedding):
        self.deleteOldRecords()
        for unknown_face in self.buffer:
            dist = facenet.distance(unknown_face['embedding'],embedding,1)
            if dist <= self.threshold:
                return True
        return False

class KnownFace(object):
    '''
    KnownFace will maintain a circular buffer of given size.
    Each slot in the buffer refers to 1 second.
    We will be deleting old messages if it exceeds the time duration(size)
    '''

    def __init__(self,size):
        self.size = size
        self.buffer = collections.deque(maxlen=size)
    
    def deleteOldRecords(self):
        current_time = int(time.time())
        while len(self.buffer) > 0 :
            knownface = self.buffer.popleft()
            last_time = knownface['time']
            # Check if time difference is greater than buffer size
            if current_time -last_time < self.size :
                self.buffer.appendleft(knownface)
                return

    def addknownface(self,employee_id):
        current_time = int(time.time())
        entry = {}
        entry['employee_id'] = employee_id
        entry['time'] = current_time
        self.buffer.append(entry)

    def match(self,employee_id):
        self.deleteOldRecords()
        for knownface in self.buffer:
            if knownface['employee_id'] == employee_id:
                return True
        return False

knownFace = KnownFace(timeWindowInSecs)
unknownFace = UnKnownFace(threshold,timeWindowInSecs)

def main(ctx,msg):
    logging.info("***** Aggregate Feed script Start *****")
    msg = json.loads(msg)
    response ={}
    response['image'] = msg['image']
    response_faces = []
    for face in msg['faces'] :
        if face['knownface'] :
            if knownFace.match(face['employee_id']) == False :
                knownFace.addknownface(face['employee_id'])
                response_faces.append(face)
            else :
                logging.info("Filtered message with employee id: %s",face['employee_id'])
        else :
            embedding = np.asarray(face['embedding'])
            if unknownFace.match(embedding) == False :
                unknownFace.addUnknownface(embedding)
                response_faces.append(face)
            else:
                logging.info("Filtered Unkown message")

    if len(response_faces) != 0 :
        response['faces'] = response_faces
        logging.info("Sent message")
        ctx.send(json.dumps(response))

    logging.info("***** Aggregate Feed script End *****")
    return
