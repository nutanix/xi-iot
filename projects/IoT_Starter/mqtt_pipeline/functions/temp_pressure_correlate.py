'''
Copyright (c) 2019 Nutanix, Inc.
Use of this source code is governed by an MIT-style license
found in the LICENSE file at https://github.com/nutanix/xi-iot.

Input:
  MQTT_TOPIC_T: {..., "airt": <temperature in Fahrenheit>, ...}
  MQTT_TOPIC_P: {..., "bar": <pressure in millibars>, ...}

'''
import json
import os

temperature = None
pressure = None

def main(ctx, msg):
    global temperature, pressure, temp_time, pressure_time
    #topic_t = ctx.get_config()["MQTT_TOPIC_T"]
    topic_t = "temp-c"
    #topic_p = ctx.get_config()["MQTT_TOPIC_P"]
    topic_p = "pressure-p"
    
    update = False
    if ctx.get_topic() == topic_t:
        temperature = json.loads(msg)["airt"]
        temp_time = ctx.get_timestamp()
        update = True
    elif ctx.get_topic() == topic_p:
        pressure = json.loads(msg)["bar"]
        pressure_time = ctx.get_timestamp()
        update = True

    if update and temperature is not None and pressure is not None:
        payload = {
            "airt_t": temp_time,
            "airt": temperature,
            "bar_t": pressure_time,
            "bar": pressure    
        }
        ctx.send(json.dumps(payload))
        