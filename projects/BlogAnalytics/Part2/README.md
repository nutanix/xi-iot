In this part we will add debezium to the project to captures the events from the mysql db generated by creating blogs and adding comments. Debezium will then feed the changes to the managed Kafka provided by the XKS platform

# Enabling Kafka
Since Kafka is a managed service provided by XKS, there is no installing required, we only have to enable it via CLI.

Create the xks manifest and apply it using the *xi-iot* CLI. Here we will enable Kafka service with default settings. For more details on custom setting please refer to the [Kafka Documentation](https://github.com/nutanix/xi-iot/tree/master/services/kafka)

[kafka-xks.yaml](kafka-xks.yaml)
```
kind: service
name: Kafka
project: Blog Analytics
serviceYaml: |
  null
```
---
Run the CLI
```
$ xi-iot create -f kafka-xks.yaml
Successfully created service: Kafka
```

Verify the installation
```
$ xi-iot get service -p 'Blog Analytics' Kafka -o yaml
kind: service
name: Kafka
project: Blog Analytics
serviceYaml: |
  null
```

# Installing Debezium
* Create an application via the Admin Console.
  **Apps and Data** -> **Kubernetes App** -> **Create** 
* Name it **debezium** and add it to the project **Blog Analytics**. 
* Add the required Service Domains to the app. 
* Use the [debezium-app.yaml](debezium-app.yaml) as the application manifest 

## Register the mysql connector
Once the debezium connector is up, we need to register the connector with mysql DB that we created in [Part1](../Part1/README.md#Installing-mysql). 

Registering requires calling a REST API on the connector, so to access that we have already enabled the Ingress as part of the debezium app.

* Register the connector by running the curl in the script below 
```
$ sh debezium-setup.sh
HTTP/1.1 201 Created
Server: nginx/1.17.8
Date: Thu, 02 Apr 2020 05:12:36 GMT
Content-Type: application/json
Content-Length: 522
Connection: keep-alive
Location: http://bloganalytics.foo.org/connectors/wordpress-connector

{"name":"wordpress-connector","config":{"connector.class":"io.debezium.connector.mysql.MySqlConnector","tasks.max":"1","database.hostname":"bloganalytics-mysql","database.port":"3306","database.user":"root","database.password":"R00tMysql","database.server.id":"184055","database.server.name":"wordpress_db","database.whitelist":"wordpress_db","database.history.kafka.bootstrap.servers":"sherlock-kafka-svc:9092","database.history.kafka.topic":"dbhistory.wordpress","name":"wordpress-connector"},"tasks":[],"type":"source"}
```

For more details on configuring debezium please refer the to [ debezium documentation](https://debezium.io/documentation/reference/1.0/connectors/mysql.html)

* Verify if the connector got registered
```
$ curl  -H "Host: bloganalytics.foo.org" http://<svc domain ip>/debezium/connectors
["wordpress-connector"]
```

* You can also view the topics created by Debezium in the Admin Console under **Data Services** -> **Kafka**

# Installing WordCloud
Wordcloud is a Python application that consumes the comments Kafka topic created by debezium from the wordpress DB and creates a wordcloud. It uses the Python [wordcloud](https://amueller.github.io/word_cloud/index.html) module.

Similar to the other apps create an Application called **wordcloud** using the Admin Console

* **Apps and Data** -> **Kubernetes App** -> **Create** 
* Add the required Service Domains to the App. 
* Use the app yaml [wordcloud-app.yaml](wordcloud-app.yaml)

We have added ingress resource to the app so it will available via the same hostname **bloganalytics.foo.org/wordcloud/**

Feel free to add comments to blog post in wordpress and see the wordcloud updated here.