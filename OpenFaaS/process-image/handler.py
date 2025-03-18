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
    """
    Function for classifying an image using the MobileNetV2 model in OpenFaaS.

    This function accepts an HTTP request with an image URL as a query parameter.
    It fetches the image from the provided URL, preprocesses it to match the input
    requirements of the MobileNetV2 model, performs inference to classify the image,
    and returns the top-3 predictions along with timing metrics.

    Args:
        event (dict): The OpenFaaS event object containing the query parameter `url`.
            - `url` (str): The URL of the image to be classified.
        context (dict): The OpenFaaS context object (not used in this function).

    Returns:
        dict: A dictionary containing:
            - `statusCode` (int): The HTTP status code of the response.
            - `body` (str): A JSON-encoded string containing:
                - `overall_duration` (float): Total time taken to process the request, in seconds.
                - `network_duration` (float): Time taken to fetch the image from the provided URL, in seconds.
                - `cpu_duration` (float): Time taken to preprocess the image (resize, normalize, etc.), in seconds.
                - `ml_duration` (float): Time taken to perform inference using the MobileNetV2 model, in seconds.
                - `predictions` (list): A list of the top-3 predictions from the model, where each prediction is a dictionary:
                    - `label` (str): The human-readable label of the predicted class (e.g., "golden retriever").
                    - `probability` (float): The confidence score of the prediction, ranging from 0 to 1.

    """
    
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
        
        # CPU-bound task: Preprocess the image
        cpu_start = time.time()
        img = image.load_img(BytesIO(response.content), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        cpu_duration = time.time() - cpu_start  # Measure just the preprocessing time

        # ML-inference task: Run prediction
        ml_start = time.time()
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        ml_duration = time.time() - ml_start
        
        overall_duration = time.time() - overall_start
        
        # Prepare the result in the same format as Azure function
        result = {
            "overall_duration": round(overall_duration, 2),
            "network_duration": round(network_duration, 2),
            "cpu_duration": round(cpu_duration, 2),
            "ml_duration": round(ml_duration, 2),
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
