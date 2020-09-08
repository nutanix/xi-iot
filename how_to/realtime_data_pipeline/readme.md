# Karbon Platform Services - DATA PIPELINES - GETTING STARTED GUIDE

## Karbon Platform Services Overview

The Nutanix Karbon Platform Services platform delivers local compute and AI edge devices, converging the edge and cloud into one seamless data processing platform. The Karbon Platform Services platform eliminates complexity, accelerates deployments, and elevates developers to focus on the business logic powering IoT applications and services. Now developers can use a low-code development platform to create application software via APIs instead of arduous programming methods.

## Introducing Data Pipelines

The main steps in this guide are excerpts from the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:Xi-IoT-Infra-Admin-Guide), available from the Nutanix Support Portal.

Data Pipelines are paths for data that include:
* **Input**. An existing data source or real-time data stream.
* **Transformation**. Code block such as a script defined in a Function to process or transform input data.
* **Output**. A destination for your data. Publish data to the cloud or cloud data service (such as AWS Simple Queue Service) at the edge.

They also enable you to process and transform captured data for further consumption or processing.

Data pipelines have the following components used in the examples in this guide:

* Data Sources (defined as MQTT in this guide)
* Runtime Environments
* Functions

### Using MQTT Data Sources in Data Pipelines

#### What is MQTT?

If you are looking to understand the internals of how MQTT works, please read the 10 part series on [MQTT Essentials](https://www.hivemq.com/tags/mqtt-essentials/) by HiveMQ.

### Adding a Data Source

You can add one or more data sources (a collection of sensors, gateways, or other input devices providing data) to associate with an edge.

Each defined data source consists of:

* Data source type (sensor, input device like a camera, or gateway) - the origin of the data
* Communication protocol typically associated with the data source
* Authentication type to secure access to the data source and data
* One or more fields specifying the data extraction method - the data pipeline specification
* Categories which are attributes that can be metadata you define to associate with the captured data

#### Add a Data Source - MQTT

* Data Extraction - MQTT
* Categories - MQTT

View these topics in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:Xi-IoT-Infra-Admin-Guide), available from the Nutanix Support Portal.

### MQTT Client Samples for Testing

If you are looking to understand the internals of how MQTT works, please read the 10 part series on [MQTT Essentials](https://www.hivemq.com/tags/mqtt-essentials/) by HiveMQ.

#### Javascript

Please refer to [mqtt package](https://www.npmjs.com/package/mqtt) and examples [here](https://github.com/mqttjs/MQTT.js/blob/master/examples/client/secure-client.js) for creating secure mqtt clients in javascript.

#### Python 2

Prerequisites

* A Nutanix edge with an IP address onboarded to Karbon Platform Services
* X509 certificates generated using Karbon Platform Services
* Python 2.7.10
* pip 10.0.1 (python 2.7)
* paho-mqtt. Install it for python 2.7.10 using the following command:

```console
$ sudo pip2.7 install paho-mqtt
```

Sample

Below is a simple example that shows how to connect to an mqtt broker, publish a single message to a specific topic and receive the published message back.

```python
# Example code to connect, publish and subscribe from a mqtt client
# For the example to work:
# 1. create a dir named 'certs' under $PWD and copy the certs
#    generated using Karbon Platform Services SaaS Portal.
# 2. Modify the 'broker_address' variable to point to the edge
#    ip address that is being used for the tests.

import paho.mqtt.client as mqttClient
import time
import ssl

def on_connect(client, userdata, flags, rc):
   if rc == 0:
      print("Connected to broker")
      global Connected
      Connected = True                #Signal connection
   else:
      print("Connection failed")

def on_publish(client, userdata, result):
   print "Published!"

def on_message(client, userdata, message):
   print "New message received!"
   print "Topic: ", message.topic
   print "Message: ", str(message.payload.decode("utf-8"))

def main():
   global Connected
   Connected = False
   # IP address of the edge. Modify this.
   broker_address= "<edge_ip>"
   port = 1883
   # NOTE: For data pipelines to receive MQTT messages, topic should
   #       be the same as that specified when creating the MQTT datasource.
   topic = "test"

   client = mqttClient.Client()
   # Set callbacks for connection event, publish event and message receive event
   client.on_connect = on_connect
   client.on_publish = on_publish
   client.on_message = on_message
   client.tls_set(ca_certs="certs/ca.crt", certfile="certs/client.crt", keyfile="certs/client.key", cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
   # Set this to ignore hostname only. TLS is still valid with this setting.
   client.tls_insecure_set(True)
   client.connect(broker_address, port=port)
   client.subscribe(topic)
   client.loop_start()

   # Wait for connection
   while Connected != True:
      print "Connecting..."
      time.sleep(1)


   try:
      client.publish(topic, "Hello, World!")
      time.sleep(5)
   except KeyboardInterrupt:
      client.disconnect()
      client.loop_stop()

if __name__ == "__main__":
   main()

```

Running the example

1. Download the certificates from Karbon Platform Services and store them locally under certs. directory. Name the files as follows:
    * ca.crt - Root CA certificate
    * client.crt - client certificate
    * client.key - client private key
1. Modify broker_address to point to the Karbon Platform Services edge IP address.
1. Run the example as follows:
```console
$ python2.7 mqtt-example.py
```
Expect output:
```console
Connecting...
Connected to broker
Published!
New message received!
Topic: test
Message: Hello, World!
```

## Runtime Environments

A runtime environment is a command execution environment to run applications written in a particular language or associated with a specific Docker registry or file. Each Function added to a Data Pipeline is executed via its own specified Runtime Environment.

Karbon Platform Services includes standard runtime environments including but not limited to the following. These runtimes are read-only and cannot be edited, updated, or deleted by users. They are available to all projects, functions, and associated container registries.

* **Golang**
* **NodeJS**
	* Node.js functions can be run in context of a data pipeline. A transformation function must accept context as well as message payload as parameters. Context can be used to query function parameters passed in when function has been instantiated. Moreover context is used to send messages to next stage in data pipeline.
	* Following is a basic Node.js function template:


```javascript
function main(ctx, msg) {
   return new Promise(function(resolve, reject) {
      // log list of transformation parameters
      console.log("Config", ctx.config)
      // log length of message payload
      console.log(msg.length)
      // forward message to next stage in pipeline
      ctx.send(msg)
      // complete promise
      resolve()
   })
}
exports.main = main
```

All functions must export main which returns a promise.

Expected output:

```console
Config { IntParam: '42', StringParam: 'hello' }
2764855
```

**Note**
Packages available in NodeJS Runtime
	* alpine-baselayout
	* alpine-keys
	* apk-tools
	* busybox
	* libc-utils
	* libgcc
	* libressl2.5-libcrypto
	* libressl2.5-libssl
	* libressl2.5-libtls
	* libstdc++
	* musl
	* musl-utils
	* scanelf
	* ssl_client
	* zlib

* **Python**
	* Functions can be executed in data pipelines to transform and filter data. Transformations are functions used to process single messages and optionally forward them to next stage in data pipeline. The next stage could be another transformation or destination of the data pipeline on edge or in the cloud. Transformation can accept parameters. In Python parameters are passed as dictionary to transformation. The following script demonstrates some basic concepts:
```python
import logging
# Python function are invoked with context and message payload.
# The context can be used to retrieve metadata about the message and allows
# function to send mesagges to next stage in stream. In this sample we just
# log message payload and forward it as is to next stage.
def main(ctx, msg):
      logging.info("Parameters: %s", ctx.get_config())
      logging.info("Process %d bytes from %s at %s", msg, ctx.get_topic(), ctx.get_timestamp())
      # Forward to next stage in pipeline.
      ctx.send(msg)
```

Pass two parameters to the function:
* MyStringParam like the name suggests is a parameter of type string.
* MyIntParam is a number.

The function would produce the following console output when processing images from a camera:
```console
[2019-03-12 04:57:26,820 root INFO] Parameters: {u'MyIntParam':u'42', u'MyStringParam': u'hello'}
[2019-03-12 04:57:26,820 root INFO] Process 2764855 bytes from rtsp://184.72.239.149:554/vod/mp4:BigBuckBunny_175k.mov at 1552366646754939017
```

**Methods provided by ctx**

* **ctx.get_config()** - returns a dict of parameters passed to the function.
* **ctx.get_topic()** - returns the topic (string) on which the current message was received. In this case, it is the topic is set to RTSP topic from which image has been received.
* **ctx.get_timestamp()** - returns the time in nanoseconds since epoch (Jan 1st, 1970 UTC).
* **ctx.send()** - Takes bytes as input and forwards it to the next stage in the pipeline. If the input is not of type bytes, an error is thrown and a corresponding alert is raised in Karbon Platform Services.

**In memory caching**
```python
import logging

counter=0

def main(ctx, msg):
      global counter
      logging.info("This is message number %d", counter)
      counter+=1
      # Forward to next stage in pipeline.
      ctx.send(msg)
```

Script produces following output:
```console
[2019-03-12 05:19:04,844 root INFO] This is message number 0
[2019-03-12 05:19:05,846 root INFO] This is message number 1
[2019-03-12 05:19:06,836 root INFO] This is message number 2
[2019-03-12 05:19:07,837 root INFO] This is message number 3
[2019-03-12 05:19:08,838 root INFO] This is message number 4
```

The data pipeline has been configured to sample every second.

Transformations are not limited to just filter or pass thru messages. A transformation can send as many messages to the next stage in pipeline as required by using context:

```python
import logging

# Transformation can send more messages than they receive.
def main(ctx, msg):
      logging.info("Process %d bytes from %s at %s", len(msg), ctx.get_topic(), ctx.get_timestamp())
      m = len(msg) / 2
      # split message in two halves
      ctx.send(msg[:m])
      ctx.send(msg[m:])
```	

Logs will reflect how message have been split:
```console
[19-03-12 05:30:51,696 root INFO] Process 2764855 bytes from rtsp://184.72.239.149:554/vod/mp4:BigBuckBunny_175k.mov
[2019-03-12 05:30:51,697 root INFO] Send 1382427 bytes
[2019-03-12 05:30:51,697 root INFO] Send 1382428 
```

**Note**

Packages available in Python 2 Runtime
* backports-abc 0.5
* elasticsearch 6.3.1
* elasticsearch-dsl 6.3.1
* futures 3.2.0
* ipaddress 1.0.22
* kafka-python 1.4.4
* msgpack 0.5.6
* nats-client 0.8.2
* paho-mqtt 1.4.0
* pip 18.1
* prometheus-client 0.5.0
* protobuf 3.6.1
* python-dateutil 2.7.5
* setuptools 40.6.3
* singledispatch 3.4.0.3
* six 1.12.0
* tornado 5.1.1
* urllib3 1.24.1
* virtualenv 16.2.0
* wheel 0.32.3
* requests 2.20.1

Packages available in Python 3 Runtime
* asyncio-nats-client 0.8.2
* elasticsearch 6.3.1
* elasticsearch-dsl 6.3.1
* kafka-python 1.4.4
* msgpack 0.5.6
* paho-mqtt 1.4.0
* pip 18.1
* prometheus-client 0.5.0
* protobuf 3.6.1
* python-dateutil 2.7.5
* setuptools 40.6.3
* six 1.12.0
* urllib3 1.24.1
* wheel 0.32.3
* requests 2.20.1

Packages available in Tensorflow Python 2 Runtime
* Absl-py 0.1.10
* astor 0.6.2
* astroid 1.6.1
* backports-abc 0.5
* backports.functools-lru-cache 1.5
* backports.shutil-get-terminal-size 1.0.0
* backports.weakref 1.0.post1
* bleach 1.5.0
* configparser 3.5.0
* cycler 0.10.0
* decorator 4.2.1
* elasticsearch 6.3.1
* elasticsearch-dsl 6.3.1
* entrypoints 0.2.3
* enum34 1.1.6
* funcsigs 1.0.2
* functools32 3.2.3.post2
* futures 3.2.0
* gast 0.2.0
* grpcio 1.10.0
* h5py 2.7.1
* html5lib 0.9999999
* imutils 0.4.5
* ipaddress 1.0.22
* ipykernel 4.8.2
* ipython 5.5.0
* ipython-genutils 0.2.0
* ipywidgets 7.1.2
* isort 4.3.3
* Jinja2 2.10
* jsonschema 2.6.0
* jupyter 1.0.0
* jupyter-client 5.2.3
* jupyter-console 5.2.0
* jupyter-core 4.4.0
* kafka-python 1.4.4
* kiwisolver 1.0.1
* lazy-object-proxy 1.3.1
* Markdown 2.6.11
* MarkupSafe 1.0
* matplotlib 2.2.2
* mccabe 0.6.1
* mistune 0.8.3
* mock 2.0.0
* msgpack 0.5.6
* nats-client 0.8.2
* nbconvert 5.3.1
* nbformat 4.4.0
* notebook 5.4.1
* numpy 1.14.0
* opencv-python 3.4.0.12
* paho-mqtt 1.4.0
* pandas 0.22.0
* pandocfilters 1.4.2
* pathlib2 2.3.0
* pbr 4.0.0
* pexpect 4.4.0
* pickleshare 0.7.4
* Pillow 5.0.0
* pip 18.1
* prometheus-client 0.5.0
* prompt-toolkit 1.0.15
* protobuf 3.5.1
* ptyprocess 0.5.2
* Pygments 2.2.0
* pylint 1.8.2
* pyparsing 2.2.0
* python-dateutil 2.7.5
* pytz 2018.3
* pyzmq 17.0.0
* qtconsole 4.3.1
* scandir 1.7
* scikit-learn 0.19.1
* scipy 1.0.0
* Send2Trash 1.5.0
* setuptools 40.6.3
* simplegeneric 0.8.1
* singledispatch 3.4.0.3
* six 1.11.0
* sklearn 0.0
* subprocess32 3.2.7
* tensorboard 1.7.0
* tensorflow 1.7.0
* termcolor 1.1.0
* terminado 0.8.1
* testpath 0.3.1
* tornado 5.1.1
* traitlets 4.3.2
* urllib3 1.24.1
* virtualenv 16.2.0
* wcwidth 0.1.7
* webencodings 0.5.1
* Werkzeug 0.14.1
* wheel 0.32.3
* widgetsnbextension 3.1.4
* wrapt 1.10.11

### Build a Custom Runtime Environment

You may need a custom runtime for some third party packages or OS distributions (like Linux) which might have dependencies not covered with the built-in Karbon Platform Services runtimes.

Like the built-in runtime environments, custom runtimes are docker images that can run functions. **A runtime container image must include the Karbon Platform Services language-specific runtime bundle.**

The bundle’s runtime environment is responsible for:

* Bootstraping the container by downloading the script assigned to that container at runtime
* Receiving messages and events
* Providing the API necessary to inspect and forward messages
* Reporting statistics and alerts to Karbon Platform Services control plane

Nutanix provides custom runtime support for three languages:
* [**Python 2**](https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python2-env.tgz)
* [**Python 3**](https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz)
* [**NodeJS**](https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/node-env.tgz)

Python 2 is distinguished from Python 3, as Python 3 syntax and libraries are not backward-compatible.

**Note**
Custom Golang runtime environments are not supported. Use the provided standard Golang runtime environment in this case.

This sample Dockerfile builds a custom runtime environment able to run Python 3 functions:
```
FROM python:3.6
RUN python -V
# Check Python version
RUN python -c 'import sys; sys.exit(sys.version_info.major != 3)'
# We need Python runtime environment to execute Python functions.
RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
RUN tar xf /python-env.tgz
# Bundle does not come with all required packages but defines them as PIP dependencies
RUN pip install -r /python-env/requirements.txt
# In this example we install Kafka client for Python as additional 3rd party software
RUN pip install kafka-python

# Containers should NOT run as root as a good practice
# We mandate all runtime containers to run as user 10001
USER 10001
# Finally run Python function worker which pull and executes functions.
CMD ["/python-env/run.sh"]
```

Build this container as usual by invoking “docker build”:
```console
$ docker build -t edgecomputing/sample-env -f Dockerfile .
Sending build context to Docker daemon   2.56kB
Step 1/9 : FROM python:3.6
Step 2/9 : RUN python -V
Step 3/9 : RUN python -c 'import sys; sys.exit(sys.version_info.major != 3)'
Step 4/9 : RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
Step 5/9 : RUN tar xf /python-env.tgz
Step 6/9 : RUN pip install -r /python-env/requirements.txt
Step 7/9 : RUN pip install kafka-python
Step 8/9 : USER 10001
Step 9/9 : CMD ["/python-env/run.sh"]
Removing intermediate container 52d45f3db900
---> 95a878cde355
Successfully built 95a878cde355
Successfully tagged edgecomputing/sample-env:latest
```

Upload the docker image to a container registry:
```console
$ docker tag edgecomputing/sample-env:latest $DOCKER_REPO/sample-env:v1.1
$ docker push $DOCKER_REPO/sample-env:v1.1
```

**Note**
Karbon Platform Services edges pull runtime images using an ‘IfNotPresent’ policy. To ensure updates are pulled, tag your container using a specific version and increment it on updates rather than relying on the ‘latest’ tag.

**Note**
Docker Hub, AWS Elastic Container Registry, and GCP Container Registry registries are supported.

#### Example Custom Runtimes

* NodeJS
```
FROM node:9

RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/node-env.tgz
RUN tar xf /node-env.tgz

WORKDIR /node-env
RUN npm install
# Containers should NOT run as root as a good practice
USER 10001
CMD ["/node-env/run.sh"]
```

* Python 3
```
FROM python:3.6

RUN python -V
# Check Python version
RUN python -c 'import sys; sys.exit(sys.version_info.major != 3)'
# We need Python runtime environment to execute Python functions.
RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
RUN tar xf /python-env.tgz
# Bundle does not come with all required packages but defines them as PIP dependencies
RUN pip install -r /python-env/requirements.txt
# In this example we install Kafka client for Python as additional 3rd party software
RUN pip install kafka-python

# Containers should NOT run as root as a good practice
# We mandate all runtime containers to run as user 10001
USER 10001
# Finally run Python function worker which pull and executes functions.
CMD ["/python-env/run.sh"]
```

Complete examples of creating custom runtimes:
* [**Python 2**](https://github.com/sharvil-kekre/xi-iot/tree/sharvil/how_to/realtime_data_pipeline/python2)
* [**Python 3**](https://github.com/sharvil-kekre/xi-iot/tree/sharvil/how_to/realtime_data_pipeline/python3)
* [**NodeJS**](https://github.com/sharvil-kekre/xi-iot/tree/sharvil/how_to/realtime_data_pipeline/nodejs)

### Creating a Runtime Environment¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Editing a Runtime Environment¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Removing a Runtime Environment¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

## Functions

A function is code used to perform one or more tasks. Supported languages include Python, Golang, and Node.js. A script can be as simple as text processing code or it could be advanced code implementing artificial intelligence, using popular machine learning frameworks like Tensorflow.

An infrastructure administrator or project user can create a function, and later can edit or clone it. You cannot edit a function that is used by an existing data pipeline. In this case, you can clone it to make an editable copy.

* When you create, clone, or edit a function, you can define one or more parameters.
* When you create a data pipeline, you define the values for the parameters when you specify the function in the pipeline.
* Data pipelines can share functions, but you can specify unique parameter values for the function in each data pipeline.

### Creating a Function¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Editing a Function¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Cloning a Function¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Removing a Function¶
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

## Implementing Data Pipelines

### Data Pipeline Visualization
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Creating a Data Pipeline
* Input - Add a Data Source
* Transformation - Add a Function
* Output - Add a Destination
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Editing a Data Pipeline
* Input - Edit a Data Source
* Transformation - Edit a Function
* Output - Edit a Destination
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

### Removing a Data Pipeline
View this topic in the [Karbon Platform Services Infrastructure Admin Guide](https://portal.nutanix.com/page/documents/details/?targetId=Xi-IoT-Infra-Admin-Guide:edg-iot-runtime-create-t.html), available from the Nutanix Support Portal.

**Note**
See [Appendix](https://nutanix.handsonworkshops.com/workshops/64d8da4f-cdeb-49f6-9722-581e446f6a96/p/#required-cloud-connector-permissions) for external permissions required to publish data via public cloud connectors.

## Appendix

### Required Cloud Connector Permissions

Karbon Platform Services requires the following permissions from each service to publish output data.

AWS S3
* s3:ListBucket: Needed for listing of existing buckets and for HEAD Bucket operation.
* s3:CreateBucket: Needed for bucket create operation if the bucket is not already present.
* s3:PutObject: Needed to write objects to S3 buckets.
Check the [S3 Permissions](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.htm) page for more details on the permissions and related actions.

AWS Kinesis
* stream:DescribeStream: Needed for checking if the Kinesis Data Stream exists and is active before attempting to write records.
* stream:CreateStream: Needed for creating a Kinesis Data Stream if it does not already exist.
* stream:PutRecord: Need for writing records to Kinesis Data Streams.
* stream:PutRecords: Need for writing a batch of records to Kinesis Data Streams.
Check the [Kinesis Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazonkinesis.html) page for more details on the permissions and related actions.

AWS SQS
* sqs:ListQueues: Needed for checking if the Queue already exists.
* sqs:CreateQueue: Needed for creating a Queue before writing to it.
* sqs:SendMessage: Needed for sending messages to a Queue.
* sqs:SendMessageBatch: Needed for sending a batch of messages to a Queue.
Check the [SQS Permissions](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-api-permissions-reference.html) page for more details on the permissions and related actions.