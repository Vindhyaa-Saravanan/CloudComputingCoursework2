import logging
from PIL import Image, ImageOps
from io import BytesIO
import requests
import base64
import time

def handle(event, context):
    start_time = time.time()
    try:
        # Extract the image URL from the query parameters
        image_url = event.query.get('url')
        if not image_url:
            return {
                "statusCode": 400,
                "body": "Missing image URL"
            }

        # Fetch the image from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        # Process the image
        image = ImageOps.fit(image, (256, 256))
        image = ImageOps.grayscale(image)
        
        # Encode the processed image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Calculate the elapsed time
        elapsed = time.time() - start_time
        return {
            "statusCode": 200,
            "body": f"Processed in {elapsed:.2f}s, image (base64): {encoded[:100]}..."
        }
    except Exception as e:
        logging.error(e)
        return {
            "statusCode": 500,
            "body": "Error processing image"
        }