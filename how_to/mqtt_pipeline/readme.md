# XI IOT - QUICK START FOR MQTT DATA PIPELINES

## Xi IoT Overview

The Nutanix Xi IoT platform delivers local compute and AI for IoT edge devices, converging the edge and cloud into one seamless data processing platform. The Xi IoT platform eliminates complexity, accelerates deployments, and elevates developers to focus on the business logic powering IoT applications and services. Now developers can use a low-code development platform to create application software via APIs instead of arduous programming methods.

SUPPORT FOR AND LEARNING MORE ABOUT XI IOT

The most support for the Xi IoT trial is available through the Nutanix Next Xi IoT trial forum. Nutanix asks that you share your experiences and lessons learned with your fellow users.

You can also visit the following pages for more information about Xi IoT.

* Connect with other users at [Xi IoT User Forum](https://next.nutanix.com/xi-iot-72).
* Connect on [Twitter](https://twitter.com/NutanixIoT) with the Nutanix Xi IoT team.
* Check out articles about Xi IoT at the [Nutanix Developer site](https://developer.nutanix.com/iot).
* View videos about Xi IoT at [Nutanix University YouTube channel](https://www.youtube.com/watch?v#wmUkz-XZLJo).
* Get more details about Xi IoT features in the [Nutanix documentation](https://portal.nutanix.com/?filterKey#type&filterVal#Xi#/page/docs/list).

### Logging On to the Xi IoT Console

Before you begin:

Supported web browsers include the current and two previous versions of Google Chrome. You’ll need your My Nutanix credentials for this step.

1. Open [https://iot.nutanix.com/](https://iot.nutanix.com/) in a web browser, click **Log in with My Nutanix** and log on with your My Nutanix credentials.
1. If you are logging on for the first time, click to read the Terms and Conditions, then click to Accept and Continue.
1. Take a few moments to read about Xi IoT, then click Get Started.

Your web browser displays the Xi IoT dashboard and the Xi IoT Quick Start Menu.

#### Creating a Project

In Xi IoT, Projects are used to segment resources such as applications and edges so that only assigned users can view and modify them. This allows different departments or teams to utilize shared data sources, edges, or cloud resources without interfering with each other.

As part of this tutorial, you’ll create a new Project to deploy your sample Data Pipelines and Applications.
1. From the **Xi IoT** management portal, select **More > Projects > + Create**.
1. Fill out the following fields and click **Next**:
    * **Name** - MQTT Pipeline
    * **Description** - Optional
    * Select + **Add Users**
    * Select your user name and click **Done**
1. Click + **Add Infrastructure**, select your Edge, and click **Done**.
Xi IoT has the ability to natively output Data Pipelines from the edge to several public cloud services such as AWS S3, or GCP Cloud Datastore. For this tutorial, Cloud Profile Selection can be left blank because no cloud resources will be used.

Xi IoT can also natively run Applications (Docker containers) at the edge using Kubernetes formated yaml as the only required input. Each yaml definition refers to a container image stored in a public or private registry. Private registries can be accessed by creating a Xi IoT Container Registry Profile to store required access information. Because this tutorial utilizes containers hosted in a public registry, Container Registry Selection can be left blank.
1. Click **Create**

#### Stagin Source Data

The tutorial depends on the availability of MQTT sample data.

Xi IoT supports direct ingest of [MQTT](https://www.hivemq.com/blog/how-to-get-started-with-mqtt/) messaging protocol (commonly used by IoT sensor devices). For other industry specific protocols, numerous hardware & software “gateways” exist to translate those data formats & protocols into MQTT.

Outside of a tutorial environment, this data would likely originate on a device external to the Edge device. However, for the purposes of the tutorial, we can leverage Xi IoT’s **Application** construct to deploy a [pre-configured containerized application](https://cloud.docker.com/u/xiiot/repository/docker/xiiot/mqtt-sensor) running directly on your Edge to generate MQTT data.

As mentioned above, Xi IoT Applications are simply Docker containers that can be deployed to the edge using Kubernetes formated yaml as the only required input. This is considered Containers-as-a-Service (CaaS) functionality and is sold as a specific Xi IoT service SKU.

### Using a Xi IoT App to Generate Sample MQTT Data

“MQTT Sensor” is a single container application that executes a python script to download a CSV file input and publish contents of each row as an MQTT message to the local Xi Edge where it is running. It can be used to test data pipeline transforms and outputs.

#### Creating the MQTT Sensor Data Source

1. If you are not logged on, open [https://iot.nutanix.com/](https://iot.nutanix.com/) in a web browser and log in.
1. Click **More > Infratructure > Data Sources.**
1. Click **+ Add Data Source.**
1. Enter **mqtt-sensor** in the Name field.
1. In the Associated Infrastructure dropdown, choose the appropriate Edge (this is the same edge where the MQTT Sensor app will run).
1. In the Protocol dropdown, choose **MQTT.**
1. Click **+ Generate Certificates**, then click **+ Download** to save the zip file to a location for reference in a future step.
1. Click **Next**.
1. On the Data Extraction page, click **Add New Field**, enter **temp** in the Name field, enter **temp** into the MQTT Topic field, click the round, blue **check**, then click **Next**.
1. Click inside the first (left) **Attribute dropdown** of the newly added category assignment and choose **Data Type**.
1. Click inside the second (right) **Attribute dropdown** of the newly added category assignment and choose **Temperature**.
1. Click **Add**.
1. On your local machine, open a shell and base64 encode the certificate bundle (zip) downloaded above. Keep the raw output available for a future step.

```
base64 -i 1561481707433_certificates.zip
```

#### Creating the MQTT Sensor Data Source

1. From the **Xi IoT** management portal, select **More > Projects > MQTT Pipeline > Apps & Data > Applications > + Create Application.**

1. Fill out the following fields and click **Next**:
    * **Name** - temp-sensor-app
    * **Description** - Optional
    * Select **+ Add Infrastructure**
    * Select your Edge and click **Select**
1. Copy and paste the [mqtt-sensor-app.yaml](https://raw.githubusercontent.com/nutanix/xi-iot/master/applications/mqtt-sensor-app/mqtt-sensor-app.yaml) into the Yaml Configuration text box.
Change the environment variables and values defined in YAML as below:
    ```
    - name: MOCK_DATA_CSV_URL
    value: "<publicly available http(s) link to data CSV>"
    - name: MQTT_INTERVAL_SEC
    value: "5"
    - name: MQTT_BROKER_IP
    value: mqttserver-svc.default
    - name: MQTT_BROKER_PORT
    value: "1883"
    - name: MQTT_TOPIC
    value: "temp"
    - name: MQTT_CLIENT_CERTIFICATES
    value: <base64 encoded certificate bundle output from earlier>
    ```
1. Click **Next**
The Input and Output page provides the option to use a YouTube-8M video or Xi IoT Sensor phone app as input and a HTTP Live Stream (HLS) as an output for applications. A user can simply check the appropriate boxes and install a [NATS](https://docs.nats.io/) client within their application. The selected input will be available on the NATS topic name stored in the NATS_SRC_TOPIC environment variable where it can be subscribed to by using the NATS server name stored in the NATS_ENDPOINT environment variable. Application output in jpeg format sent to the topic name stored in NATS_DST_TOPIC will be available via the application’s HTTP Live Stream. For this tutorial, both boxes should remain unchecked because these features will not be used.
1. Click **Create.**
1. Click **mqtt-sensor-app** to see a Summary of the application performance, alerts, deployments, etc.

Infrastructure Deployments should list “1 of 1 Running” on your Edge device once the application has successfully launched.

#### Deploying Function

Xi IoT Functions allow developers to directly build and execute business logic to correlate, filter, or transform data in standard languages such as Python or Go without the burden of maintaining underlying operating systems or runtimes.

1. From the **Xi IoT** management portal, select **More > Projects > MQTT Pipeline > Apps & Data > Functions > + Add Function.**
1. Fill out the following fields to create the first function:
    * **Name** - temp-filter
    * **Description** - Optional
    * **Project** - MQTT Pipeline
    * **Language** - Python
    * **Runtime Environment** - Python2 Env
Xi IoT Functions may be written in well known software languages most commonly used for edge computing and machine learning. These currently include Python, Go, and Node.js. This allows developers to re-use existing code, or quickly write new logic utilizing standard libraries, all without the burden of learning a new platform or language.
1. Click **Next**
1. Copy and paste [temp_filter.py](https://raw.githubusercontent.com/nutanix/xi-iot/master/projects/mqtt_pipeline/functions/temp_filter.py) into the Function text box.
1. Clicke **Create**
