#!/usr/bin/python
'''
Copyright (c) 2018 Nutanix, Inc.
Use of this source code is governed by an MIT-style license 
found in the LICENSE file at https://github.com/nutanix/xi-iot.

This example Function may be used in a ML training use case or any use case where payloads
recieved on multiple topics need to be correlated. It ingests an image payload
(i.e. GigE Vision or RTSP) on the "images" topic and stores it in memory. If a new label 
to correlate is received on the "labels" topic, its combined with the image payload and 
returned as a single JSON payload.

Each message received in the pipeline results in an invocation of the
function(s) in the pipeline. The functions have to be written as shown below:
main(ctx, msg):
  ...

main() will be invoked for every new message received in the pipeline.

Args:
1. ctx - context object that has the following methods defined on it.
    1.1. get_topic() - returns the MQTT topic on which the payload was received.
                       Useful if same pipeline receives from multiple topics.
    1.2. get_selector() - returns the categories defined on the topic.
    1.3. get_timestamp() - returns the timestamp at which the payload was received by Sherlock edge.
    1.4. get_payload() - returns the payload received on the topic.
    1.5. send() - used to send the processed output back onto the pipeline. Needs bytes as input.

2. msg - payload, same as the returned by ctx.get_payload()
'''
import logging
import numpy
import sys
import cv2
import msgpack
import base64
import json

def init():
    '''
    Globals can be used to store payloads in memory for use as multiple messages arrive.
    This init function is called when the pipeline is created or updated.
    '''
    global image_payload
    global label_payload
    #set globals to init
    logging.info("***** Setting globals to init *****")
    image_payload = "init"
    label_payload = "init"
    return

init()

def main(ctx,msg):
    global image_payload
    global label_payload
    
    if ctx.get_topic() == "images":
        '''
        Use get_topic to determine the MQTT topic.
        If we receive an image message then store the payload in image_payload global.
        '''
        logging.info("***** Image message received *****")
        logging.info("***** Unpacking message *****")
        unpacked_dict = msgpack.unpackb(msg, raw=True)
        image = numpy.fromstring(unpacked_dict["Data"], dtype=unpacked_dict["DataType"])
        image = image.reshape((unpacked_dict["Height"],unpacked_dict["Width"],unpacked_dict["Channels"]))
        _, img_encoded = cv2.imencode('.jpg', image)
        encodedStr = base64.b64encode(img_encoded)
        logging.info("***** Storing unpacked frame payload in memory *****")
        payload ={}
        payload['timestamp'] = ctx.get_timestamp()
        payload['image'] = encodedStr
        image_payload = payload
        return
    elif ctx.get_topic() == "labels":
        logging.info("***** Label message received *****")
        if image_payload == "init":
            logging.info("***** Label message received, but no image payload in memory *****")
        else:
            #If we receive a label and have image_payload then combine them.
            logging.info("***** Retrieving unpacked frame payload from memory *****")
            payload ={}
            payload['image_timestamp'] = image_payload['timestamp']
            payload['image'] = image_payload['image']
            logging.info("***** Adding label payload to image payload *****")
            payload['label_timestamp'] = ctx.get_timestamp()
            payload['label'] = msg
            #Return the combined payload as a single JSON.
            return ctx.send(json.dumps(payload))
    else:
        return