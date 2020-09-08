# Using RTSP in Karbon Platform Services

## Data Source
The following steps will show you how to set up an RTSP camera as a data source in Karbon Platform Services:
1. Log into the Karbon Platform Services Cloud Management Console and click **Infrastructure** → **Data Sources**, and then **+Add Data Source**.
1. Complete information on the General tab and then click Next.
    * Name: enter a name for your camera
    * Associated edge: choose the edge that will connect to the camera feed
    * Protocol: RTSP
    * Authentication: choose **Username and Password**
    * IP Address: enter the IP address of the camera
    * User Name: enter the username for the camera
    * Password: enter the password for the camera
1. Complete information on the Data Extraction tab and then click **Next**.
    * Click Add New Field
    * In the new Field row, enter a Name for the feed (i.e VideoFeed)
    * In the new Field row, enter the RTSP URL of your camera and click the round check box.
1. Complete the information on the **Attributes** tab and click **Create**.
    * From the Select Fields dropdown, choose **All Fields**
    * From the Attribute dropdown, choose **Data Type** and then **Image**
1. You can now use your RTSP camera as a data source in an application or data pipeline. 

## What is RTSP?
If you are looking to understand the internals of how RTSP works, please read this [documentation](https://tools.ietf.org/html/rfc2326) by The Internet Society.
