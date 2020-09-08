import ssl
import time
import random
import msgpack
from tensorflow import keras
import paho.mqtt.client as mqttClient


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")
		global Connected                #Use global variable
		Connected = True                #Signal connection 
	else:
		print("Connection failed")

def on_publish(client, userdata, result):
	print("Published!")

def on_message(client, userdata, message):
	print("New message received!")
	print("Topic:", message.topic)
	print("Message:", message)


def main():
	global Connected
	Connected = False
	# IP address of the edge. Modify this.
	broker_address= "<edge ip>"
	port = 1883
	# NOTE: For data pipelines to receive MQTT messages, topic should
	#       be the same as that specified when creating the MQTT datasource.
	input_topic = "apparel_images"
	output_topic = "apparel-predict"

	client = mqttClient.Client()
	# Set callbacks for connection event, publish event and message receive event
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.on_message = on_message
	client.tls_set(ca_certs="certs/ca.crt", certfile="certs/client.crt", keyfile="certs/client.key", cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
	# Set this to ignore hostname only. TLS is still valid with this setting.
	client.tls_insecure_set(True)
	client.connect(broker_address, port=port)
	client.subscribe(outpu_topic)
	client.loop_start()

	# Wait for connection
	while Connected != True:
		print("Connecting...")
		time.sleep(1)

	fashion_mnist = keras.datasets.fashion_mnist
	(images, image_labels), (test, labels) = fashion_mnist.load_data()

	# scale the values to 0.0 to 1.0
	images = images / 255.0
	# reshape for feeding into the model
	images = images.reshape(images.shape[0], 28, 28, 1)

	for i in range(10):
		print(f'\nCounter: {i+1}')
		img = random.choice(images)
		print(img.shape)
		payload ={}
		payload['image'] = img.tolist()
		payload['dtype'] = str(images.dtype)
		payload['height'] = 28
		payload['width'] = 28
		try:
			client.publish(input_topic, msgpack.packb(payload))
			time.sleep(5)
		except KeyboardInterrupt:
			client.disconnect()
			client.loop_stop()

if __name__ == "__main__":
	 main()