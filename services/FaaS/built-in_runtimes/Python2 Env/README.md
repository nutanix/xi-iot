# A simple Python2 Transformation

Scripts can be executed in data pipelines to transform and filter data.
Transformations are functions used to process single messages and optionally forward them to next stage in data pipeline.
The next stage could be another transformation or destination of the data pipeline on edge or in the cloud.
Transformation can accept parameters. In Python parameters are passed as dictionary to transformation.

The following script demonstrates some basic concepts:

```
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

We chose to pass two parameters to the function:

* MyStringParam like the name suggests is a parameter of type string.
* MyIntParam is a number.

The script would produce the following console output when processing images from a camera:

> [2019-03-12 04:57:26,820 root INFO] Parameters: {u'MyIntParam': u'42', u'MyStringParam': u'hello'}

> [2019-03-12 04:57:26,820 root INFO] Process 2764855 bytes from rtsp://184.72.239.149:554/vod/mp4:BigBuckBunny_175k.mov at 1552366646754939017

### Methods provided by ctx
* **ctx.get_config()** - returns a dict of parameters passed to the function.
* **ctx.get_topic()** - returns the topic (string) on which the current message was received. In this case, it is the topic is set to RTSP topic from which image has been received.
* **ctx.get_timestamp()** - returns the time in nanoseconds since epoch (Jan 1st, 1970 UTC).
* **ctx.send()** - Takes `bytes` as input and forwards it to the next stage in the pipeline. If the input is not of type `bytes`, an error is thrown and a corresponding alert is raised in Karbon Platform Services.

### In memory caching
Unlike other serverless frameworks, state can be cached in running transformation to allow for aggregation across multiple messages.
Following is a demonstration of state in functions:

```
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

> [2019-03-12 05:19:04,844 root INFO] This is message number 0

> [2019-03-12 05:19:05,846 root INFO] This is message number 1

> [2019-03-12 05:19:06,836 root INFO] This is message number 2

> [2019-03-12 05:19:07,837 root INFO] This is message number 3

> [2019-03-12 05:19:08,838 root INFO] This is message number 4

Clearly data pipeline has been configured to sample every second.

Transformation are not limited to just filter or pass thru messages.
A transformation can send as many messages to next stage in pipeline as required by using context:

```
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

> 19-03-12 05:30:51,696 root INFO] Process 2764855 bytes from rtsp://184.72.239.149:554/vod/mp4:BigBuckBunny_175k.mov

> [2019-03-12 05:30:51,697 root INFO] Send 1382427 bytes

> [2019-03-12 05:30:51,697 root INFO] Send 1382428 bytes

### Packages available in Python2 runtime
* backports-abc==0.5
* elasticsearch==6.3.1
* elasticsearch-dsl==6.3.1
* futures==3.2.0
* ipaddress==1.0.22
* kafka-python==1.4.4
* msgpack==0.5.6
* nats-client==0.8.2
* paho-mqtt==1.4.0
* pip==18.1
* prometheus-client==0.5.0
* protobuf==3.6.1
* python-dateutil==2.7.5
* setuptools==40.6.3
* singledispatch==3.4.0.3
* six==1.12.0
* tornado==5.1.1
* urllib3==1.24.1
* virtualenv==16.2.0
* wheel==0.32.3
* requests==2.20.1

