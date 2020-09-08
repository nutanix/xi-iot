# How to build and deploy a custom runtime

Nutanix Karbon Platform Services ships with built-in runtime environments that support scripts designed to run in those environments. However, you might need a custom runtime for some third party packages or OS distributions (like Linux) which might have dependencies not covered with the built-in Karbon Platform Services runtimes.

Like the built-in runtime environments, custom runtimes are docker images that can run scripts.
A runtime container image must include our language-specific runtime bundle.

The bundle's runtime environment is responsible for:

- Bootstrapping the container by downloading the script assigned to that container at runtime
- Receiving messages and events
- Providing the API necessary to inspect and forward messages
- Reporting statistics and alerts to Karbon Platform Services control plane

Nutanix provides custom runtime support for three languages:

- Python2 (https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python2-env.tgz)
- Python3 (https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz)
- NodeJS (https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/node-env.tgz)

We distinguish between Python2 and 3, as Python 3 syntax and libraries are not backward-compatible.

This sample Dockerfile builds a custom runtime environment able to run Python3 functions.

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

Build this container as usual by invoking "docker build".

```
$ docker build -t edgecomputing/sample-env -f Dockerfile .
Sending build context to Docker daemon   2.56kB
Step 1/9 : FROM python:3.6
 ---> 1a604f0a8780
Step 2/9 : RUN python -V
 ---> Running in 99717fadbdb0
Python 3.6.8
Removing intermediate container 99717fadbdb0
 ---> 247d2bf923b5
Step 3/9 : RUN python -c 'import sys; sys.exit(sys.version_info.major != 3)'
 ---> Running in da4cc664a50e
Removing intermediate container da4cc664a50e
 ---> 775d43d37d05
Step 4/9 : RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
 ---> Running in b4bc66d5efbf
--2019-03-13 05:29:59--  https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
Resolving s3-us-west-2.amazonaws.com (s3-us-west-2.amazonaws.com)... 52.218.193.120
Connecting to s3-us-west-2.amazonaws.com (s3-us-west-2.amazonaws.com)|52.218.193.120|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1597975 (1.5M) [application/x-tar]
Saving to: ‘python-env.tgz’

     0K .......... .......... .......... .......... ..........  3%  335K 5s
    50K .......... .......... .......... .......... ..........  6% 3.29M 2s
   100K .......... .......... .......... .......... ..........  9%  729K 2s
   150K .......... .......... .......... .......... .......... 12% 3.46M 2s
   200K .......... .......... .......... .......... .......... 16% 6.44M 1s
   250K .......... .......... .......... .......... .......... 19%  886K 1s
   300K .......... .......... .......... .......... .......... 22% 5.07M 1s
   350K .......... .......... .......... .......... .......... 25% 9.30M 1s
   400K .......... .......... .......... .......... .......... 28% 5.13M 1s
   450K .......... .......... .......... .......... .......... 32% 4.84M 1s
   500K .......... .......... .......... .......... .......... 35% 1.47M 1s
   550K .......... .......... .......... .......... .......... 38% 4.06M 1s
   600K .......... .......... .......... .......... .......... 41% 2.80M 1s
   650K .......... .......... .......... .......... .......... 44% 12.8M 1s
   700K .......... .......... .......... .......... .......... 48% 4.03M 0s
   750K .......... .......... .......... .......... .......... 51% 24.7M 0s
   800K .......... .......... .......... .......... .......... 54% 11.6M 0s
   850K .......... .......... .......... .......... .......... 57% 30.8M 0s
   900K .......... .......... .......... .......... .......... 60% 11.0M 0s
   950K .......... .......... .......... .......... .......... 64% 9.12M 0s
  1000K .......... .......... .......... .......... .......... 67% 6.16M 0s
  1050K .......... .......... .......... .......... .......... 70% 4.31M 0s
  1100K .......... .......... .......... .......... .......... 73% 10.8M 0s
  1150K .......... .......... .......... .......... .......... 76% 5.14M 0s
  1200K .......... .......... .......... .......... .......... 80% 15.5M 0s
  1250K .......... .......... .......... .......... .......... 83% 2.23M 0s
  1300K .......... .......... .......... .......... .......... 86% 10.6M 0s
  1350K .......... .......... .......... .......... .......... 89% 10.1M 0s
  1400K .......... .......... .......... .......... .......... 92% 4.39M 0s
  1450K .......... .......... .......... .......... .......... 96% 10.4M 0s
  1500K .......... .......... .......... .......... .......... 99% 4.05M 0s
  1550K ..........                                            100% 71.2M=0.5s

2019-03-13 05:30:00 (2.84 MB/s) - ‘python-env.tgz’ saved [1597975/1597975]

Removing intermediate container b4bc66d5efbf
 ---> 9bb73fb0c3e2
Step 5/9 : RUN tar xf /python-env.tgz
 ---> Running in edb23c2d521b
Removing intermediate container edb23c2d521b
 ---> 66012245e8af
Step 6/9 : RUN pip install -r /python-env/requirements.txt
 ---> Running in 187d8153c1ab
Collecting asyncio-nats-client==0.8.2 (from -r /python-env/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/f6/a0/3e9a55cfe262699a2ce98714e14a7381bc674112f567af80457d16ea9b2f/asyncio-nats-client-0.8.2.tar.gz
Collecting elasticsearch==6.3.1 (from -r /python-env/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/b1/f1/89735ebb863767516d55cee2cfdd5e2883ff1db903be3ba1fe15a1725adc/elasticsearch-6.3.1-py2.py3-none-any.whl (119kB)
Collecting elasticsearch-dsl==6.3.1 (from -r /python-env/requirements.txt (line 3))
  Downloading https://files.pythonhosted.org/packages/d3/ee/b748249edf415573cc66a8203318b4f7f8a4246e5a562d5f77985f11db4c/elasticsearch_dsl-6.3.1-py2.py3-none-any.whl (48kB)
Collecting kafka-python==1.4.4 (from -r /python-env/requirements.txt (line 4))
  Downloading https://files.pythonhosted.org/packages/5f/89/f13d9b1f32cc37168788215a7ad1e4c133915f6853660a447660393b577d/kafka_python-1.4.4-py2.py3-none-any.whl (255kB)
Collecting msgpack==0.5.6 (from -r /python-env/requirements.txt (line 5))
  Downloading https://files.pythonhosted.org/packages/22/4e/dcf124fd97e5f5611123d6ad9f40ffd6eb979d1efdc1049e28a795672fcd/msgpack-0.5.6-cp36-cp36m-manylinux1_x86_64.whl (315kB)
Collecting paho-mqtt==1.4.0 (from -r /python-env/requirements.txt (line 6))
  Downloading https://files.pythonhosted.org/packages/25/63/db25e62979c2a716a74950c9ed658dce431b5cb01fde29eb6cba9489a904/paho-mqtt-1.4.0.tar.gz (88kB)
Collecting pip==18.1 (from -r /python-env/requirements.txt (line 7))
  Downloading https://files.pythonhosted.org/packages/c2/d7/90f34cb0d83a6c5631cf71dfe64cc1054598c843a92b400e55675cc2ac37/pip-18.1-py2.py3-none-any.whl (1.3MB)
Collecting prometheus-client==0.5.0 (from -r /python-env/requirements.txt (line 8))
  Downloading https://files.pythonhosted.org/packages/bc/e1/3cddac03c8992815519c5f50493097f6508fa153d067b494db8ab5e9c4ce/prometheus_client-0.5.0.tar.gz
Collecting protobuf==3.6.1 (from -r /python-env/requirements.txt (line 9))
  Downloading https://files.pythonhosted.org/packages/c2/f9/28787754923612ca9bfdffc588daa05580ed70698add063a5629d1a4209d/protobuf-3.6.1-cp36-cp36m-manylinux1_x86_64.whl (1.1MB)
Collecting python-dateutil==2.7.5 (from -r /python-env/requirements.txt (line 10))
  Downloading https://files.pythonhosted.org/packages/74/68/d87d9b36af36f44254a8d512cbfc48369103a3b9e474be9bdfe536abfc45/python_dateutil-2.7.5-py2.py3-none-any.whl (225kB)
Collecting setuptools==40.6.3 (from -r /python-env/requirements.txt (line 11))
  Downloading https://files.pythonhosted.org/packages/37/06/754589caf971b0d2d48f151c2586f62902d93dc908e2fd9b9b9f6aa3c9dd/setuptools-40.6.3-py2.py3-none-any.whl (573kB)
Collecting six==1.12.0 (from -r /python-env/requirements.txt (line 12))
  Downloading https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Collecting urllib3==1.24.1 (from -r /python-env/requirements.txt (line 13))
  Downloading https://files.pythonhosted.org/packages/62/00/ee1d7de624db8ba7090d1226aebefab96a2c71cd5cfa7629d6ad3f61b79e/urllib3-1.24.1-py2.py3-none-any.whl (118kB)
Requirement already satisfied: wheel==0.32.3 in /usr/local/lib/python3.6/site-packages (from -r /python-env/requirements.txt (line 14)) (0.32.3)
Collecting requests==2.20.1 (from -r /python-env/requirements.txt (line 15))
  Downloading https://files.pythonhosted.org/packages/ff/17/5cbb026005115301a8fb2f9b0e3e8d32313142fe8b617070e7baad20554f/requests-2.20.1-py2.py3-none-any.whl (57kB)
Collecting idna<2.8,>=2.5 (from requests==2.20.1->-r /python-env/requirements.txt (line 15))
  Downloading https://files.pythonhosted.org/packages/4b/2a/0276479a4b3caeb8a8c1af2f8e4355746a97fab05a372e4a2c6a6b876165/idna-2.7-py2.py3-none-any.whl (58kB)
Collecting chardet<3.1.0,>=3.0.2 (from requests==2.20.1->-r /python-env/requirements.txt (line 15))
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
Collecting certifi>=2017.4.17 (from requests==2.20.1->-r /python-env/requirements.txt (line 15))
  Downloading https://files.pythonhosted.org/packages/60/75/f692a584e85b7eaba0e03827b3d51f45f571c2e793dd731e598828d380aa/certifi-2019.3.9-py2.py3-none-any.whl (158kB)
Building wheels for collected packages: asyncio-nats-client, paho-mqtt, prometheus-client
  Building wheel for asyncio-nats-client (setup.py): started
  Building wheel for asyncio-nats-client (setup.py): finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/97/c2/d8/9e7feb1cf61461b68cc6d7dc07ff20dfa52fbd20d01e9e5b25
  Building wheel for paho-mqtt (setup.py): started
  Building wheel for paho-mqtt (setup.py): finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/82/e5/de/d90d0f397648a1b58ffeea1b5742ac8c77f71fd43b550fa5a5
  Building wheel for prometheus-client (setup.py): started
  Building wheel for prometheus-client (setup.py): finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/1a/74/d7/dc59e0bf44fdfd6395c0076129453abf563e4aeca5d72c8574
Successfully built asyncio-nats-client paho-mqtt prometheus-client
Installing collected packages: asyncio-nats-client, urllib3, elasticsearch, six, python-dateutil, elasticsearch-dsl, kafka-python, msgpack, paho-mqtt, pip, prometheus-client, setuptools, protobuf, idna, chardet, certifi, requests
  Found existing installation: pip 19.0.1
    Uninstalling pip-19.0.1:
      Successfully uninstalled pip-19.0.1
  Found existing installation: setuptools 40.8.0
    Uninstalling setuptools-40.8.0:
      Successfully uninstalled setuptools-40.8.0
Successfully installed asyncio-nats-client-0.8.2 certifi-2019.3.9 chardet-3.0.4 elasticsearch-6.3.1 elasticsearch-dsl-6.3.1 idna-2.7 kafka-python-1.4.4 msgpack-0.5.6 paho-mqtt-1.4.0 pip-18.1 prometheus-client-0.5.0 protobuf-3.6.1 python-dateutil-2.7.5 requests-2.20.1 setuptools-40.6.3 six-1.12.0 urllib3-1.24.1
Removing intermediate container 187d8153c1ab
 ---> be516801b0bd
Step 7/9 : RUN pip install kafka-python
 ---> Running in c2aa25015d91
Requirement already satisfied: kafka-python in /usr/local/lib/python3.6/site-packages (1.4.4)
You are using pip version 18.1, however version 19.0.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container c2aa25015d91
 ---> 28dccb38c6ab
Step 8/9 : USER 10001
 ---> Running in c4a466d2b322
Removing intermediate container c4a466d2b322
 ---> 670f18d44955
Step 9/9 : CMD ["/python-env/run.sh"]
 ---> Running in 52d45f3db900
Removing intermediate container 52d45f3db900
 ---> 95a878cde355
Successfully built 95a878cde355
Successfully tagged edgecomputing/sample-env:latest
```

Next, upload the docker image to a container registry. Here, we use AWS Elastic Container Registry (ECR) in this example:

```
$ docker tag edgecomputing/sample-env:latest $DOCKER_REPO/sample-env:latest
$ docker push $DOCKER_REPO/sample-env:latest

```
