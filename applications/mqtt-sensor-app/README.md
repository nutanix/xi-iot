# MQTT Sensor

Simple application to create mock MQTT data using CSV input.

## Overview

“MQTT Sensor” is a single container application that executes a python script to download a CSV file input and publish contents of each row as an MQTT message
to the local Xi Edge where it is running. It can be used to test data pipeline transforms and outputs.

## Getting it up and running

1. Via the Karbon Platform Services Management Console, create a new MQTT Data Source.
    - Choose Associated Infrastructure (Edge) (This is the same edge where the MQTT Sensor app will run).
    - Generate & download its certificates.
    - Add a new field and assign the MQTT topic.
    - Add any required data source categories to the field.
2. Base-64 encode the certificate bundle (zip) downloaded in step 1.
    - ```base64 -i 1561481707433_certificates.zip```
3. Via the Karbon Platform Services Management Console create a new Application within the same Project to which the Associated Infrastructure (Edge) in step 1 is also assigned.
    - Choose the same Associated Infrastructure (Edge) from step 1.
    - Import the mqtt-sensor-app.yaml and modify the below environment variables as needed.

    ```env:
        - name: MOCK_DATA_CSV_URL
          value: "<publicly available http(s) link to data CSV>"
        - name: MQTT_INTERVAL_SEC
          value: "5"
        - name: MQTT_BROKER_IP
          value: mqttserver-svc.default
        - name: MQTT_BROKER_PORT
          value: "1883"
        - name: MQTT_TOPIC
          value: "<topic to publish on>"
        - name: MQTT_CLIENT_CERTIFICATES
          value: <base64 encoded certificate bundle>
    ```
## Advanced configuration

## Official documentation

## Usage examples

## References

## Troubleshooting
### Server logging

## Known limitations and plans

## Contribution

### Contribution rules

All contributed code must be compatible with the [MIT](https://github.com/nutanix/xi-iot/blob/master/LICENSE) license.

All changes needs to have passed style, unit and functional tests.

All new features need to be covered by tests.

### Building

### Testing

## Contact

Submit Github issue to ask question, request a feature or report a bug.


