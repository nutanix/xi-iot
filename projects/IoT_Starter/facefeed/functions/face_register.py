# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

import json
import logging

def main(ctx,msg):
    input_data = json.loads(msg)
    response = {}
    response['name'] = input_data['name']
    response['designation'] = input_data['designation']
    response['department'] = input_data['department']
    response['employee_id'] = input_data['employee_id']
    response['face'] = input_data['faces'][0]['face']
    response['embedding'] = input_data['faces'][0]['embedding']
    logging.info("Successfully Registered Employee with ID: %s",input_data['employee_id'])
    return ctx.send(json.dumps(response))