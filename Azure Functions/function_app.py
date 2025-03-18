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
def classify_image(req: func.HttpRequest) -> func.HttpResponse:
    overall_start = time.time()
    try:
        image_url = req.params.get('url')
        if not image_url:
            return func.HttpResponse("Missing image URL", status_code=400)
        
        # Network-bound task: Fetch the image.
        network_start = time.time()
        response = requests.get(image_url)
        network_duration = time.time() - network_start
        
        # CPU-bound task: Preprocess the image and run inference.
        cpu_start = time.time()
        # Load and resize image to 224x224 (expected size for MobileNetV2)
        img = image.load_img(BytesIO(response.content), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        cpu_duration = time.time() - cpu_start
        
        overall_duration = time.time() - overall_start
        
        result = {
            "overall_duration": round(overall_duration, 2),
            "network_duration": round(network_duration, 2),
            "cpu_duration": round(cpu_duration, 2),
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
