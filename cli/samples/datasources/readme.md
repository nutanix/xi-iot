# Creating a Data Source

Read about data source and category details and requirements in the [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide).

## Example Usage

Create a data source with attributes you've defined in a YAML file.

`user@host$ kps create -f my-mqtt-datasource.yaml`

# Creating The Data Source YAML File

These example YAML files define a Karbon Platform Services category and data source type of MQTT (Message Queuing Telemetry Transport lightweight messaging protocol) or RTSP (real-time streaming protocol).

## mqtt-datasource.yaml

``` yaml
kind: category
name: mqtt-data
description: category for mqtt data
values:
  - input
---
kind: dataSource
name: mqtt-sfo-datasource
protocol: MQTT
authType: CERTIFICATE
edge: sfo-edge1 
fields:
- name: cats
  topic: cat-images
selectors:
- categoryName: mqtt-data
  categoryValue: input
  scope:
    - cats
```

## rtsp-datasource.yaml

``` yaml
kind: category
name: rtsp-data
description: category for rtsp data
values:
  - input
---
kind: dataSource
name: rtsp-sfo-datasource
protocol: RTSP
authType: PASSWORD
edge: sfo-edge2 
fields:
- name: dogs
  topic: rtsp://user1:password1/dog-images
selectors:
- categoryName: rtsp-data
  categoryValue: input
  scope:
    - dogs
```    


## Define a Category to Help Organize Captured Data

The first `kind: category` YAML entity creates and defines the data source category used by the `kind: dataSource` YAML entity. The category is associated with data or files captured from the data source.

- Create a category named `mqtt-data` or `rtsp-data` as specified in the `name` field.
- Categorize data by labeling it as part of the `values` field. You can then specify one or more labels for your data source. This sample specifies just one value: `input` . You can add as many value labels as you need. 

This YAML category entity is optional. You can optionally create a separate category YAML file with this information if you just want to create a category and do not want to create a data source at the same time. If you include this YAML code chunk in a YAML file where you define a data source, you can use this file to create a category *and* create a data source at the same time.

## Define Your Data Source

The second `kind: dataSource` YAML entity is required to create the data source. It defines the data source attributes and associated Karbon Platform Services edge.

Each data source consists of:

- A user-defined `name` (no spaces; lowercase with underscore or dash characters preferred)
- Communication `protocol` associated with the data source. Specify `MQTT` or `RTSP`.
- Authentication type `authType` to secure access to the data source and data. See definitions below.
- A topic `fields` A list of fields with a field name and topic name. For example, in case of MQTT, topic is the name of the topic being streamed to an MQTT server. A field name is required for category association of data streaming into the given topic.
- A category `categoryName` and one or more of its category labels `categoryValue:` `selector` is a list of category key value pairs plus a scope. Incoming data is tagged with a category key/value based on a scope field name. Other Karbon Platform Services entities like data pipelines can also receive data using this same category key/value.


| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `dataSource` | Specify the resource type  |
| name |     | Unique name for your data source |
| description |     | Describe your data source |
| protocol  | `mqtt` or `rtsp` | Specify the protocol for your data source |
| authType |  | Secure the connection between your data source and the Karbon Platform Services edge |
|  | `CERTIFICATE` | For MQTT, use `CERTIFICATE`. Specify the certificate on the command line |
|  | `PASSWORD` | For RTSP, use  `PASSWORD`. Specify the user email address and password in the RTSP topic. Example: `rtsp://user@contoso.com:password/dog-images` |
| edge |  | Specify the Karbon Platform Services edge to be associated with this data source |
| fields |  | Data to be extracted from this data source |
|  | name | Topic name |
|  | topic | MQTT topic: A case-sensitive UTF-8 string. An MQTT topic name must be unique when creating an MQTT data source. You cannot duplicate or reuse an MQTT topic name for multiple MQTT data sources. Example: `cat-images`to identify cats. |
|  |  | RTSP topic: An RTSP stream name must be unique. You cannot duplicate or reuse an RTSP protocol stream name for multiple RTSP data sources. Specify the user email address and password in the URL |
| selectors |  | A list of category key value pairs plus a scope. Incoming data is tagged with a category key/value based on a scope field name. Other Karbon Platform Services entities like data pipelines can also receive data using this same category key/value. |
|  | categoryName | Name of your existing category |
|  | categoryValue | Category key value as defined in this YAML file or in a separate YAML file, here: `input`. |
|  | scope | Specific data type for the captured data.  |
|  |  |  |
