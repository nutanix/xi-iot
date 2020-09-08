# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

import numpy as np
from PIL import Image
import logging
import cv2
import base64
import io
import time
import json
from threading import Thread
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import sys
from facerecognition import facenet


#esIP = "10.15.232.225"
esIP = "elasticsearch"
esPort = 9200
esIndex = "datastream-faceregister"
threshold = 0.27893

class FaceMatch(object):

    def __init__(self,threshold):
        self.knownfaces = []
        self.threshold = threshold

    def update_known_faces(self,faces):
        self.knownfaces = faces

    def match(self,face):
        closest_face = None
        min_dist = 1
        for known_face in self.knownfaces:
            #dist = np.sqrt(np.sum(np.square(np.subtract(known_face['embedding'], face))))
            dist = facenet.distance(known_face['embedding'],face,1)
            logging.info("Calculated distance (%f) with employee id:%s",dist,known_face['employee_id'])
            if dist < min_dist :
                closest_face = known_face
                min_dist = dist
        if min_dist <= self.threshold:
            logging.info("Found matching face with distance: %f",min_dist)
            return closest_face
        return 

class FetchKnownFaces(Thread):
    def __init__(self,esIP,esPort,esIndex,facematch):
        Thread.__init__(self)
        self.esIndex = esIndex
        self.esIP = esIP
        self.esPort = esPort
        self.facematch = facematch
    def connect(self):
        self.esclient = Elasticsearch([{'host': self.esIP, 'port': self.esPort}])

    def run(self):
        s = Search(using=self.esclient, index=self.esIndex)
        count =0
        while True:
            try:
                #response = s.execute(True)
                response =[]
                for hit in s.scan():
                    response.append(hit)
                if count % 10 == 0:
                    count = 0
                    logging.info("Fetched registered faces from Elastic Search. Number of records found: %d",len(response))
                facematch.update_known_faces(response)
                count = count +1
            except Exception as e:
                logging.exception("Failed to get registered faces from Elastic Search.")
            # Sleep for 60 secs
            time.sleep(60)

facematch = FaceMatch(threshold)
updateThread = FetchKnownFaces(esIP,esPort,esIndex,facematch)
updateThread.setDaemon(True)
updateThread.connect()
updateThread.start()

def main(ctx,msg):
    logging.info("***** Face Match script Start *****")
    msg = json.loads(msg)
    data = msg['data']
    image = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
    cvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    faces = msg['faces']
    # Returning if we don't find any face.  
    if len(faces) == 0:
        logging.info("No face found")
        logging.info("***** Face match script End *****")
        return
    for i in range(len(faces)):
        known_face = facematch.match(np.asarray(faces[i]['embedding']))
        bb = faces[i]['bb']
        if known_face is None:
            faces[i]['knownface'] = False
            cv2.rectangle(cvImage,(bb[0], bb[1]), (bb[2], bb[3]),(0, 0,255), 2)
        else:
            faces[i]['knownface'] = True
            faces[i]['name'] = known_face['name']
            faces[i]['designation'] = known_face['designation']
            faces[i]['department'] = known_face['department']
            faces[i]['employee_id'] = known_face['employee_id']
            logging.info("Found matching face with employee id: %s",known_face['employee_id'])
            cv2.rectangle(cvImage,(bb[0], bb[1]), (bb[2], bb[3]),(0, 255, 0), 2)
    response ={}
    if len(faces) !=0 :
        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', cvImage)
        encodedStr = base64.b64encode(img_encoded)
        response['image'] = encodedStr
        response['faces'] = faces
        logging.info("Idenitfied %d faces",len(faces))
    else:
        response['image'] = data
        response['faces'] = faces
    ctx.send(json.dumps(response))
    logging.info("***** Face match script End *****")
    return


'''
#Test
if __name__ == '__main__':
    faces = json.load(open('../tests/test.json'))
    for i in range(len(data)):
        known_face = facematch.match(np.asarray(data[i]['embedding']))
        if known_face is None:
            data[i]['knownface'] = False
        else:
            data[i]['knownface'] = True
            data[i]['name'] = known_face[i]['name']
        logging.info(data[i]) 
'''