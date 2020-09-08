# Creating an Application

Read more about application details and requirements in the [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide).

You can create intelligent applications to run on the Karbon Platform Services edge or cloud instance cloud where you have pushed collected data.

## Example Usage

Create an application with attributes defined in a YAML file. An application requires Karbon Platform Services edge or Karbon Platform Services cloud instance.

`user@host$ kps create -f echo-ifc-app.yaml`

## echo-sample-app.yaml

``` yaml
kind: application
name: echo-sample-app
description: my sample app
project: Starter
appYamlPath: echoserver-k8s.yaml 
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `application` | Specify the resource type  |
| name |     | Unique name for your application |
| description |     | Describe your application |
| project  |  | Specify an existing project by project name to associate with this resource. If project uses an explicit edge association, specify the edges also. See the next sample YAML file for reference |
| appYamlPath |  | Specify the k8s yaml file path for your app. The path could be absolute or relative to the location of Karbon Platform Services YAML file. |

## echo-ifc-app.yaml

``` yaml
# Note: This sample requires a Karbon Platform Services cloud instance or deployments. See https://www.nutanix.com/products/iot
kind: application
name: echo-ifc-app
description: echo app
project: Starter
edges:
- sjc-edge1 
appYamlPath: echoserver-k8s.yaml
dataIfcEndpoints:
  - dataSource: youtube-8m # consume youtube data source as a stream of jpegs
    topicName: https://www.youtube.com/watch?v=HqqsJkonXsA # copy this url from the UI for now
    fieldName: youtube-8m-1  # consume youtube video for field name=youtube-8m-1
  - dataSource: live-stream # publish jpegs to this 
    topicName: my-echo-app # enter anything here
    fieldName: my-echo-app # enter anything here
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `application` | Specify the resource type  |
| name |     | Unique name for your application |
| description |     | Describe your application |
| project  |  | Specify an existing project by project name to associate with this resource |
| edges | `sjc-edge1`   | Specify the Karbon Platform Services edge where the apps will run. Note: It is mandatory to specify edges if project to edge association is explicit. That is, projects are bound to edges based on explicit edge association, rather than based on category selectors |
| appYamlPath |  | Specify the k8s yaml path for your app. The path could be absolute or relative to the location of Karbon Platform Services yaml |
| dataIfcEndpoints | | A list of dataIfcEndpoints that define a data source, along with field/topic that this app has access to. A single entry in this list can point to an input DataIfcEndpoint. That is, the app can consume data from it. <br /> Or, it can point to an output DataIfcendpoint, that is, app can output data to it. At this time, the Karbon Platform Services cloud instance only supports two DataIfcEndpoints: youtube (input) and live-stream (output) |
| dataIfcEndpoints | | A list of dataIfcEndpoints that define a data source, along with field/topic that this app has access to. A single entry in this list can point to an input DataIfcEndpoint. That is, the app can consume data from it. <br /> Or, it can point to an output DataIfcendpoint, that is, app can output data to it. At this time, the Karbon Platform Services cloud instance only supports two DataIfcEndpoints: youtube (input) and live-stream (output) |
||dataSource| Name of the data source. Options are `youtube-8m`, `live-stream`. For an input dataIfcEndpoint like `youtube-8m`, jpegs can be consumed from NATS topic pointed to by the env NATS_SRC_TOPIC inside your app container. Similarly, for an output dataIfcEndpoint like `live-stream`, the platform will expose env NATS_DST_TOPIC inside your app container.
|| topicName| For `youtube-8m`, topicName is the URL of the YouTube video. Note: this URL should already be set on the  `youtube-8m` data source through the Karbon Platform Services management console. For `live-stream`, topicName can be the same as fieldName and is created on the fly by the platform.
||fieldName| For `youtube-8m`, fieldName would be the same as fieldName on the Karbon Platform Services management console that is already populated. For `live-stream`, pick any name or string.
