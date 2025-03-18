import logging
from io import BytesIO
import requests
import time
import json
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Load the MobileNetV2 model with pretrained weights on ImageNet.
model = MobileNetV2(weights='imagenet')

def handle(event, context):
    overall_start = time.time()
    try:
        # Extract the image URL from query parameters
        image_url = event.query.get('url')
        if not image_url:
            return {
                "statusCode": 400,
                "body": "Missing image URL"
            }
        
        # Network-bound task: Fetch the image
        network_start = time.time()
        response = requests.get(image_url)
        network_duration = time.time() - network_start
        
        # CPU-bound task: Preprocess the image and run inference
        cpu_start = time.time()
        img = image.load_img(BytesIO(response.content), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        cpu_duration = time.time() - cpu_start
        
        overall_duration = time.time() - overall_start
        
        # Prepare the result in the same format as Azure function
        result = {
            "overall_duration": round(overall_duration, 2),
            "network_duration": round(network_duration, 2),
            "cpu_duration": round(cpu_duration, 2),
            "predictions": [
                {"label": pred[1], "probability": float(pred[2])} for pred in predictions
            ]
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        logging.error(e)
        return {
            "statusCode": 500,
            "body": "Error processing image"
        }
