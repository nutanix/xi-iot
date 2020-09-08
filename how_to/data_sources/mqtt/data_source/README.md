# Creating an MQTT datasource in Karbon Platform Services
MQTT datasource in Karbon Platform Services enables a data pipeline to receive data from any
device that can send MQTT messages. An example of such a device would be an
industrial sensor or gateway that wants to publish data to a Karbon Platform Services edge for
processing data in a pipeline.

### Steps
Go to `Data Source` page in Karbon Platform Services and click on `Add Data Source`. Creating a datasource
involves 3 distinct steps.  

**1. General**
* Enter the name of the datasource
* Select the edge to which this datasource is to be associated. The IP of this edge will be the IP of the MQTT broker too.
* Set `Protocol` to `MQTT`
* Click on `Generate Certificates`. This will generate new set of X509 certificates and make them downloadable. Download these certificates and use them with the MQTT client that will publish messages to or receive messages from the edge.  

**2. Data Extraction**
* Click on `Add New Field` to create a new field.
* Under `Name`, enter a human readable name for the MQTT topic.
* Under `MQTT Topic`, enter the MQTT topic name that will be used. This same topic name is to be used by the MQTT client for publishing message. **NOTE** MQTT topic names are case sensitive.

**3. Category Assignment**
* Assign a category to the field entered in the previous step. These categories are human redable tags (key:value pairs) associated with the MQTT topic. An infra admin will be able to create categories for use in this step.