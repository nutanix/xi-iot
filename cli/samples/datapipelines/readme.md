# Creating a Data Pipeline

Read about data pipeline details and requirements in the [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide).

Each sample YAML file defines a data pipeline. A data pipeline consists of:

- Input. An existing data source or real-time data stream (output from another data pipeline).
- Transformation. Code block such as a script defined in a Function to process or transform input data. See [Functions](../functions).
- Output. A destination for your data. Publish data to the cloud or cloud data service (such as AWS, Google, or Azure) at the edge.

## Example Usage

Create a data pipeline with attributes defined in a YAML file.

`user@host$ kps create -f mqtt-input-s3-output.yaml`

## mqtt-input-s3-output.yaml

This sample data pipeline consumes data from an MQTT data source, uses a function to transform the data, then defines a cloud destination for the transformed data (in this case an AWS S3 bucket).


``` yaml
# mqtt -> s3
kind: dataPipeline
name: mqtt-to-s3-pipeline
description: This data pipeline consumes data from MQTT, then outputs to an AWS S3 bucket
project: Starter
samplingIntervalMsec: 1
functions:
- name: echo-param-fn
  args:
    param1: foo # pass argument param1=foo
input:
  categorySelectors:
    mqtt-data:
      - input
output:
  publicCloud:
    type: AWS
    service: S3
    region: us-west-2
    endpointName: mqtt-to-s3 # Specify the endpoint AWS S3 bucket name
    profile: my-aws-profile # you would need to add this profile to project=Starter using UI for now. Ref: https://portal.nutanix.com/#/page/docs/details?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-onboarding-add-cloud-t.html
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `dataPipeline` | Specify the resource type |
| name |     | Unique name for your resource type |
| description |     | Describe your resource type |
| project  | | Specify an existing project by project name to associate with this resource |
| samplingIntervalMsec |  |  Specify a data sampling interval in milliseconds |
| functions |  | Specify one or more functions to transform your captured data |
|  | name | Function name |
|  | args | Parameters or arguments to pass to your function |
|  |  | param1. Pass a parameter or argument to your function. Specify each parameter on a separately line. In this example, you would specify param2 on a separate line for second parameter |
| input  |  | Specify the available data type to consume, according to an existing category.|
|  | categorySelectors |  In this sample, pipeline consumes data tagged with category mqtt-data and value=input |
| output  |  | The destination for the transformed data in this case is a cloud instance (publicCloud). For this example, `AWS` sends the data to Amazon AWS |
|  | publicCloud |  |
|  | type | Here, `AWS`. Other cloud types you can specify are `GCP` and `Azure` |
|  | service | Here, S3. Other AWS services you can specify are Kinesis, SQS. Other available service types: <br /> For type `Azure`:  `Blob` <br /> For type `GCP`: `PubSub` , `CloudSQL` , CloudDataStore  |
|  | region | Specify the cloud service region name. |
|  | endpointName | Here, name of the AWS S3 bucket.  For other services, it would also map to the name of the entity for the corresponding service. |
|  | profile | Specify the name of your cloud profile. The [Karbon Platform Services Admin Guide](https://portal.nutanix.com/#/page/docs/details?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-onboarding-add-cloud-t.html) describes how to create your cloud profile. |

## mqtt-input-azure-blob-output.yaml

This sample data pipeline consumes data from an MQTT data source, then defines a cloud instance destination for the transformed data (in this case an Azure blob).

``` yaml
kind: dataPipeline
name: azure-cli-pipeline
description: Azure blob output pipeline
project: Default Project 
input:
  categorySelectors:
    mqtt-data:
      - input
output:
  publicCloud:
    type: Azure
    service: Blob
    endpointName: az-cli-pipeline
    profile: my-azure-profile
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `dataPipeline` | Specify the resource type |
| name |     | Unique name for your resource type |
| description |     | Describe your resource type |
| project  | | Specify an existing project by project name to associate with this resource |
| input  |  | Specify the available data type to consume, according to an existing category |
|  | categorySelectors |  In this sample, pipeline consumes data tagged with category mqtt-data and value=input |
| output  |  | The destination for the transformed data in this case is a cloud instance (publicCloud). For this example, `Azure` sends the data to Azure blob storage. |
|  | publicCloud |  |
|  | type | Here, `Azure`. |
|  | service | Here, `Blob` indicates Azure blob storage |
|  | endpointName | Here, name of the Azure blob |
|  | profile | Specify the name of your cloud profile. The [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide) describes how to create your cloud profile. |

## mqtt-input-local-kafka-output.yaml

This sample data pipeline consumes incoming data from an MQTT data source, uses a function to transform the data, then defines its destination as a Kafka service available at the Karbon Platform Services edge.


``` yaml
kind: dataPipeline
name: mqtt-to-kafka
description: This data pipeline consumes incoming data from MQTT and outputs it to a Kafka service at the edge
project: Starter
samplingIntervalMsec: 1
functions:
- name: echo-param-fn
  args:
    param1: foo # pass argument param1=foo
input:
  categorySelectors:
    mqtt-data:
      - input
output:
  localEdge:
    type: DataService
    service: Kafka
    endpointName: mqtt-to-kafka # Specify the Kafka topic name
```    

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `dataPipeline` | Specify the resource type |
| name |     | Unique name for your resource type |
| description |     | Describe your resource type |
| project  | | Specify an existing project by project name to associate with this resource |
| samplingIntervalMsec |  |  Specify a data sampling interval in milliseconds |
| functions |  | Specify one or more functions to transform your captured data |
|  | name | Function name |
|  | args | Parameters or arguments to pass to your function |
|  |  | param1. Pass a parameter or argument to your function. Specify each parameter on a separate line. In this example, you would specify param2 on a separate line for second parameter |
|  |  |  |
| input |  | Specify the available data type to consume, according to an existing category |
|  | categorySelectors |  In this sample, pipeline consumes data tagged with category mqtt-data and value=input |
| output |  | The destination for the transformed data here is a Karbon Platform Services edge. |
|  | localEdge | Output type of localEdge defines output destination for services running on the edge where this data pipeline is deployed |
| type | Here, `DataService`. Other options include: <br /> `RealTimeStreaming` -  outputs the data to the real time streaming service on the edge. <br />  `DataInterface` - (available for a Karbon Platform Services Cloud instance only) outputs data to a data interface like HLS (HTTP live streaming) |
|  | service | Here, `Kafka` indicates in the service available at the edge. Other options include MQTT, RTSP, HLS |
|  | endpointName | Here, kafka topic name. In other cases, this would be the entity name or identifier for the corresponding edge service |

## concat-pipelines.yaml

Stream data from the MQTT through concatenated data pipelines, eventually writing the data to Kinesis

This sample data pipeline includes two YAML entities named `pipeline1` and `pipeline2` to form a concatenated pipeline. 

- `pipeline1` consumes data based on mqtt-data category, then sends transformed data to the real-time streaming service running on the Karbon Platform Services edge
- `pipeline1` output provides the input data for `pipeline2` through the RealTimeStreaming service, which further transforms that data and sends the result to an AWS Kinesis stream

``` yaml
# mqtt -> pipeline1 -> pipeline2 -> Kinesis
kind: dataPipeline
name: pipeline1
description: This data pipeline takes MQTT data as input and outputs to a real-time streaming service
project: Starter
samplingIntervalMsec: 1
functions:
- name: echo-param-fn
  args:
    param1: foo # pass argument param1=foo
input:
  categorySelectors:
    mqtt-data:
      - input
output:
  localEdge:
   type: DataService
   service: RealTimeStreaming
   endpointName: mqtt-to-realtimestream
---
kind: dataPipeline
name: pipeline2
description: This data pipeline consumes pipeline1 output as its input, then outputs to an AWS Kinesis stream
project: Starter
samplingIntervalMsec: 1
functions:
- name: echo-param-fn
  args:
    param1: foo # pass argument param1=foo
input:
  dataPipeline: pipeline1
output:
  publicCloud:
    type: AWS
    service: Kinesis
    region: us-west-2
    endpointName: pipeline2-to-kinesis # Specify a Kinesis stream name
    profile: my-aws-profile # you must  create add this profile to project=Starter using UI for now: https://portal.nutanix.com/#/page/docs/details?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-onboarding-add-cloud-t.html . Add your cloud profile to a project described here: https://portal.nutanix.com/#/page/docs/details?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-projects-c.html
```
### pipeline1
1. The first YAML entity `pipeline1` creates a data pipeline that samples MQTT data every millisecond. The sampled data is transformed by the `echo-param-fn` function. 
2. The destination for the transformed data is the RealTimeStreaming service endpoint named `mqtt-to-realtimestream` running on this edge.

### pipeline2
1. The second YAML entity `pipeline2` creates a data pipeline that consumes `pipeline1` output from the Karbon Platform Services edge real-time streaming service endpoint.
2. It samples that streaming data every millisecond. The sampled data is again transformed by the `echo-param-fn` function.
3. The destination for the transformed data is an a cloud instance: AWS Kinesis endpoint named `pipeline2-to-kinesis`.

Note: The [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide) describes how to create your cloud profile and add your [cloud profile to a project] (https://portal.nutanix.com/#/page/docs/details?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-projects-c.html).
