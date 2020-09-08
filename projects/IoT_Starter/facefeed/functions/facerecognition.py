# Copyright (c) 2018 Nutanix, Inc.
# Use of this source code is governed by an MIT-style license 
# found in the LICENSE file at https://github.com/nutanix/xi-iot.

# Parts of this code utilize the Inception ResNet v1 model pre-trained
# from the VGGFace2 training dataset, and were adapted from the Facenet 
# example at https://github.com/davidsandberg/facenet 




import base64
import cStringIO
import json
import io
from PIL import Image
import tensorflow as tf
import numpy as np
from facerecognition import facenet
from facerecognition.align import detect_face
import cv2
import logging


# some constants kept as default from facenet
minsize = 20
threshold = [0.6, 0.7, 0.7]
factor = 0.709
margin = 44
input_image_size = 160
blur_detection_threshold = 100


sess = tf.Session()

# read pnet, rnet, onet models from align directory and files are det1.npy, det2.npy, det3.npy
pnet, rnet, onet = detect_face.create_mtcnn(sess, '/mllib/facerecognition/align')

# read 20180402-114759 model file downloaded from https://drive.google.com/file/d/1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-/view
facenet.load_model("/mllib/facerecognition/20180402-114759/20180402-114759.pb")

# Get input and output tensors
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]

def blur_image(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_map = cv2.Laplacian(gray_image, cv2.CV_64F)
    score = np.var(blur_map)
    if score < blur_detection_threshold :
        return True
    return False


def getFaces(img):
    faces = []
    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    if not len(bounding_boxes) == 0:
        for face in bounding_boxes:
            if face[4] > 0.80:
                det = np.squeeze(face[0:4])
                bb = np.zeros(4, dtype=np.int32)
                # left
                bb[0] = np.maximum(det[0] - margin / 2, 0)
                # top
                bb[1] = np.maximum(det[1] - margin / 2, 0)
                # right
                bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                # bottom
                bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                height = bb[3] - bb[1]
                width = bb[2] - bb[0]
                bb_threshold = -40
                # Don't consider face ,if the dimensions is less than the required image size
                if (height - input_image_size < bb_threshold) or (width - input_image_size < bb_threshold) :
                    logging.info("Skipping face because the detected box is small. height: %f, width: %f",height,width)
                    continue
                cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
                resized = cv2.resize(cropped, (input_image_size,input_image_size),interpolation=cv2.INTER_CUBIC)
                # Check if image is blurred
                if blur_image(resized):
                    logging.info("Blurred Image")
                    continue

                prewhitened = facenet.prewhiten(resized)
                embedding = getEmbedding(prewhitened)
                listEmbedding = embedding.tolist()
                # encode image as jpeg
                _, img_encoded = cv2.imencode('.jpg', resized)
                encodedStr = base64.b64encode(img_encoded)
                top = np.int32(bb[0]).item()
                left = np.int32(bb[1]).item()
                bottom = np.int32(bb[2]).item()
                right = np.int32(bb[3]).item()
                faces.append({'face':encodedStr,'bb':[top,left,bottom,right],'embedding':listEmbedding})
    return faces
def getEmbedding(resized):
    reshaped = resized.reshape(-1,input_image_size,input_image_size,3)
    feed_dict = {images_placeholder: reshaped, phase_train_placeholder: False}
    embedding = sess.run(embeddings, feed_dict=feed_dict)
    return embedding

def detect_faces(data):
  #image = Image.open(image_path).convert('RGB')
  image = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
  cvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
  return getFaces(cvImage)


def main(ctx,msg):
    logging.info("***** Face Recognition script Start *****")
    input_data = json.loads(msg)
    faces = detect_faces(input_data['data'])
    input_data['faces'] = faces
    logging.info("Detected number of faces: %d",len(faces))
    logging.info("***** Face Recognition script End *****")
    return ctx.send(json.dumps(input_data))
