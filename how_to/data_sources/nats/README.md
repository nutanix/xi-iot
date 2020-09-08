## NATS Data Interface

The *nats* data interface can be used to connect the NATS resources you have set up on the edge to Karbon Platform Services. To start setting up this datasource, use the following example YAML and create your data source via the Karbon Platform Services CLI.

**nats.yaml**
```yaml
kind: dataSource
name: ex_nats
svcDomain: <Service Domain>
protocol: DATAINTERFACE
type: Sensor
authType: CERTIFICATE
ifcInfo:
  class: DATAINTERFACE
  img: dataifc/nats:v1.0
  kind: IN
  protocol: nats
  ports:
    - name: nats
      port: 4222
edge: myprovideredge
fields:
- name: topic
  topic: "<Device Topic>"
- name: port
  topic: "natsport-4222"
```

**Note:** Your *Device Topic* is the NATS address your device communicates with. 

Run the following command to create an instance of the datasource:
```console
kps create -f nats.yaml
```
* If the yaml was configured correctly, you should now see a datasource in your UI called *ex-nats*.
* This device can now be leveraged as a data source in entities such as Kubernetes Applications and Data Pipelines.

### Litmus Edge

The NATS data interface can also be used to integrate with [Litmus Edge](https://litmus.io/litmus-edge/) to enable a wide range of [device and protocol data sources](https://litmus.io/litmus-edge/supported-devices/) with minor adjustments. 
The following YAML file is configured to connect with Litmus Edge.

**litmus.yaml**
```yaml
kind: dataSource
name: litmus
svcDomain: <Service Domain>
protocol: DATAINTERFACE
type: Sensor
authType: CERTIFICATE
ifcInfo:
  class: DATAINTERFACE
  img: dataifc/nats:v1.0
  kind: IN
  protocol: nats
  ports:
    - name: nats
      port: 4222
edge: myprovideredge
fields:
- name: secret
  topic: "<LoopEdge Secret>"
- name: host
  topic: "<LoopEdge Address>"
- name: port
  topic: "natsport-4222"
```

If your LoopEdge information was configured correctly, your device names and topics should now be in the cloud as artifacts.
To see your newly created artifacts run the following command:
```console
kps get datasource --show-artifacts
```

You should be met with a row entry labelled *litmus*. Inside this row entry you should see a list of your device tags and corresponding device topics:
```console
NAME         	ENDPOINTS                                             CLIENT SECRET  
litmus        	<names>:                                                   
              		devicehub.raw.<topic>.*                 
                <names>:                                                          
               		devicehub.raw.<topic>.*
```

Proceed to add required device topics directly in the Karbon Platform Services UI. Proceed to **Infrastructure** → **Data Sources** and click on *litmus*. 
Select **Edit** and you should be brought to a menu where you can define your data source topics. You should see your some topics such as port and secret already present. Now you 
can add the device topic of your choice and select **Update**.
* Once you have updated your data source, you will start ingesting data from your selected device and use this entity in Kubernetes Applications and Data Pipelines.

## NATS FAQs

What happens if a device topic is removed and a new one added?
* The stream will be immediately cancelled and the data source will start ingesting data from the new device topic.

Can topics from multiple devices be added to the same Karbon Platform Services data source?
* No, it is recommended to create multiple data sources for each unique device topic. External gateway devices or software (like Litmus Edge) may also be used to aggregate data from multiple sources. 

Is there a way to ingest multiple device and protocol (i.e. PLC) sources as one Karbon Platform Services data source?
* Yes, multiple devices can be configured under one device topic in Litmus Edge.