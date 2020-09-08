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

