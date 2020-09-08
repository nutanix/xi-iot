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
   logging.info("***** Converting C to F *****")
   payload["airt"] = 9.0/5.0 * float(payload["airt"]) + 32
   return ctx.send(json.dumps(payload))