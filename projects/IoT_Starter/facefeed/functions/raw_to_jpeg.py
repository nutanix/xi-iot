# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

import numpy
import sys
import cv2
import msgpack
import base64
import json

def main(ctx,msg):
    unpacked_dict = msgpack.unpackb(msg, raw=False, max_bin_len=3145728)
    image =  numpy.fromstring(unpacked_dict["Data"], dtype=unpacked_dict["DataType"])
    image = image.reshape((unpacked_dict["Height"],unpacked_dict["Width"],unpacked_dict["Channels"]))
    cvImage = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    _, img_encoded = cv2.imencode('.jpg', cvImage)
    encodedStr = base64.b64encode(img_encoded)
    payload ={}
    payload['data'] = encodedStr
    ctx.send(json.dumps(payload))
    return
