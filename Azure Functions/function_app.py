import azure.functions as func 
import logging
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO
import requests
import base64
import time
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="process_image")
def process_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    overall_start = time.time()
    try:
        image_url = req.params.get('url')
        if not image_url:
            return func.HttpResponse("Missing image URL", status_code=400)
        
        # Task 1: Network-bound operation: Fetch the image
        network_start = time.time()
        response = requests.get(image_url)
        network_duration = time.time() - network_start
        
        # Task 2: CPU-bound operation: Preprocessing the image
        cpu_start = time.time()
        image = Image.open(BytesIO(response.content))
        image = ImageOps.fit(image, (256, 256))
        image = ImageOps.grayscale(image)
        cpu_duration = time.time() - cpu_start
        
        # Task 3: ML inference task: Edge detection (using a filter as a proxy for ML inference)
        ml_start = time.time()
        edge_image = image.filter(ImageFilter.FIND_EDGES)
        ml_duration = time.time() - ml_start
        
        # Encode the final image (after edge detection)
        buffered = BytesIO()
        edge_image.save(buffered, format="JPEG")
        encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        overall_duration = time.time() - overall_start
        
        result = {
            "overall_duration": round(overall_duration, 2),
            "network_duration": round(network_duration, 2),
            "cpu_duration": round(cpu_duration, 2),
            "ml_inference_duration": round(ml_duration, 2),
            "encoded_image": encoded
        }
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Error processing image", status_code=500)
