# Kafka Data Service

We provide support for Kafka which is an extensible streaming platform. Clients can manage, publish and subscribe to topics using the native Kafka protocol.

Data Pipelines can use Kafka as destination. Similarly applications can use Kafka client of their choice to access the Kafka Data Service.

## Instantiate a Kafka Data Service

Services are enabled per project to be consumed by Pipelines and Kubernetes Applications within that project. Moreover Kafka can optionally be exposed for external clients.

A sophisticated data service like Kafka has many config options which a user might want to change from their default values. We allow various settings to be tuned for throughput, latency, availability or durability reasons. We treat all Kafka brokers as equals. That is all brokers will have same configuration settings.

You can configure Kafka by using the common service API. The CLI supports this API which we'll demonstrate shortly. 

### A simple Kafka instance with default settings

The service can be instantiated using CLI as follows:

```
# Enable Kafka service in project "MyProject"
$ kps service enable kafka -p MyProject
# Disable Kafka service in project "MyProject"
$ kps service disable kafka -p KafkaTest
```

### A Kafka instance with custome settings

```
# Configuration parameters in YAML format
$ cat kafka.yaml
nodePort: 32093
logRetentionHours: 1
kafkaVolumeSize: 60Gi
# Enable Kafka service in project “MyProject”
$ kps service enable kafka -f kafka.yaml -p MyProject
```

Of course, deleting the service might affect running applications and data pipelines.

## Access Kafka Data Service from Pipelines

Data Pipelines can specify Kafka as destination. Pipelines will use Kafka cluster enabled for the project. If no Kafka cluster has been explicitly enabled for project, a new cluster will be instantiated with default settings.

## Access Kafka Data Service from Kubernetes Applications

Applications are not required to discover Kafka clusters. We rely on applications templating for injecting actual Kafka broker list into applications:

```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: my-kafka-app
spec:
  template:
    metadata:
      labels:
        app: my-kakfa-app
    spec:
      containers:
      - name: some-container
        image: my-kafka-app
        env:
        - name: KAFKA_SERVER
          value: "{{.Services.Kafka.Endpoint}}"
        ports:
        - containerPort: 9000
```

KAFKA_SERVER will be expanded to Kafka API endpoint as a headless k8s service. That is, a DNS A entry with IPs for each broker in the cluster.

Kafka deployments come with their own Zookeeper Ensemble. Similar to Kafka API endpoint, Zookeeper's endpoint is injected into app YAML by using template parameter.

```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: kafdrop
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: kafdrop
    spec:
      containers:
      - name: kafdrop
        image: thomsch98/kafdrop
        env:
        - name: LISTEN
          value: "9000"
        - name: ZK_HOSTS
          value: "{{.Services.KafkaZookeeper.Endpoint}}"
        ports:
        - containerPort: 9000
---
apiVersion: v1
kind: Service
metadata:
  name: kafdrop
  annotations:
    sherlock.nutanix.com/http-ingress-path: /kafdrop
spec:
  ports:
  - port: 9000
  selector:
    app: kafdrop

```

This app YAML starts Kafdrop, a Kafka UI on any Service Domain.

## Access Kafka Data Service from external clients

External clients must specify a list of Kafka brokers (IP:port) as usual for Kafka clients. We publish list of Kafka endpoints in UI.

To see externally exposed Kafka brokers for your project: From the Projects page in the Karbon Platform Services cloud management console, click your project name. Open Data Services > Kafka and click the Deployments tab.

## Kafka settings

Following is a list of all settings and their defaults values. Change config default settings with caution since those affect availability and durability of Kafka data.

```
nodePort: 0 (must be valid k8s node port 30000-32767 or 0)
kafkaVolumeSize: 6Gi
zookeeperVolumeSize: 2Gi
kafkaMemory: 512M
zookeeperMemory: 512M
kafkaCPU: 500m
zookeeperCPU: 500m
logRetentionHours: 168
logRetentionBytes: -1
```