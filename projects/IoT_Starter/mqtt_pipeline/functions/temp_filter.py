# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

import logging
import json

'''
Example payload
   payload = '{
    "deviceId": "D13",
    "airt": 85,
    "unit": "F" }'
'''
def main(ctx,msg):
   payload = json.loads(msg)
   #Filter temperature greater than 80F
   if float(payload["airt"]) >=65:
            logging.info("***** Temp >= 65: Forwarding Payload *****")
            return ctx.send(json.dumps(payload))
   logging.info("***** Temp < 65: Dropping Payload *****")
   return ""
