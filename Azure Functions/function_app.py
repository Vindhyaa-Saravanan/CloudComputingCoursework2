import azure.functions as func 
import logging
import time
import json
import requests
from io import BytesIO

import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Load the MobileNetV2 model with pretrained weights on ImageNet.
model = MobileNetV2(weights='imagenet')

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="classify_image")
    """Route for classifying an image using MobileNetV2.
    This function accepts an HTTP GET request with an image URL as a query parameter.
    It fetches the image from the provided URL, preprocesses it to match the input
    requirements of the MobileNetV2 model, performs inference to classify the image,
    and returns the top-3 predictions along with timing metrics.

    Args:
        req (func.HttpRequest): The HTTP request object containing the query parameter `url`.
            - `url` (str): The URL of the image to be classified.

    Returns:
        func.HttpResponse: An HTTP response object containing:
            - `overall_duration` (float): Total time taken to process the request, in seconds.
            - `network_duration` (float): Time taken to fetch the image from the provided URL, in seconds.
            - `cpu_duration` (float): Time taken to preprocess the image (resize, normalize, etc.), in seconds.
            - `ml_duration` (float): Time taken to perform inference using the MobileNetV2 model, in seconds.
            - `predictions` (list): A list of the top-3 predictions from the model, where each prediction is a dictionary:
                - `label` (str): The human-readable label of the predicted class (e.g., "golden retriever").
                - `probability` (float): The confidence score of the prediction, ranging from 0 to 1.
    """
def classify_image(req: func.HttpRequest) -> func.HttpResponse:
    
    overall_start = time.time()
    try:
        # Extract the image URL from query parameters
        image_url = req.params.get('url')
        if not image_url:
            return func.HttpResponse("Missing image URL", status_code=400)
        
        # Network-bound task: Fetch the image
        network_start = time.time()
        response = requests.get(image_url)
        network_duration = time.time() - network_start
        
        # CPU-bound task: Preprocess the image
        cpu_start = time.time()
        # Load and resize image to 224x224 (expected size for MobileNetV2)
        img = image.load_img(BytesIO(response.content), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        cpu_duration = time.time() - cpu_start 

        # ML-inference task: Run prediction
        ml_start = time.time()
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        ml_duration = time.time() - ml_start
        
        overall_duration = time.time() - overall_start
        
        # Return results as structured JSON response
        result = {
            "overall_duration": round(overall_duration, 2),
            "network_duration": round(network_duration, 2),
            "cpu_duration": round(cpu_duration, 2),
            "ml_duration": round(ml_duration, 2),
            "predictions": [
                {"label": pred[1], "probability": float(pred[2])} for pred in predictions
            ]
        }
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Error processing image", status_code=500)
