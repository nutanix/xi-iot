import os
import json
import logging
import requests
import msgpack
import numpy as np

logging.getLogger().setLevel(logging.INFO)
ai_inference_endpoint = os.environ['AI_INFERENCE_ENDPOINT']
logging.info("Apperal Classifier")

# class labels 
class_map = {
        0 : 'T-shirt/top', 
        1 : 'Trouser', 
        2 : 'Pullover', 
        3 : 'Dress', 
        4 : 'Coat',
        5 : 'Sandal', 
        6 : 'Shirt', 
        7 : 'Sneaker', 
        8 : 'Bag', 
        9 : 'Ankle boot'
}

def predict(image):
    data = json.dumps({"signature_name": "serving_default",
                       "instances": [image]})
    headers = {"content-type": "application/json"}
    model_name = "fashion_classifier"
    model_version = 1
    url = "http://%s/v1/models/%s/versions/%d:infer" % (ai_inference_endpoint, model_name, model_version)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        logging.error(response.json())
        return None
    inference_payload = json.loads(response.content)
    pred_array = inference_payload['predictions'][0]
    pred_index = pred_array.index(max(pred_array))
    prediction = class_map[pred_index]
    return prediction, max(pred_array)

def main(ctx, msg):
	payload = msgpack.unpackb(msg)
	img = payload['image']
	prediction, confidence = predict(img)
	output = "Prediction: {}, Confidence: {}".format(prediction, str(confidence))
	logging.info(output)
	ctx.send(msg)
	return