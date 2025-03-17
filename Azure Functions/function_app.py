import azure.functions as func
import logging
from PIL import Image, ImageOps
from io import BytesIO
import requests
import base64
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="process_image")
def process_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start_time = time.time()
    try:
        image_url = req.params.get('url')
        if not image_url:
            return func.HttpResponse("Missing image URL", status_code=400)

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image = ImageOps.fit(image, (256, 256))
        image = ImageOps.grayscale(image)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')

        elapsed = time.time() - start_time
        return func.HttpResponse(f"Processed in {elapsed:.2f}s, image (base64): {encoded[:100]}...", status_code=200)
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Error processing image", status_code=500)