import requests
import time
import csv
import json

# Function URLs
AZURE_FUNCTION_URL = "https://vin-image-processing-workflow.azurewebsites.net/api/classify_image"
OPENFAAS_FUNCTION_URL = "http://20.26.125.107:8080/function/process-image"
                      
# Define a set of image sizes (width x height) to test
image_sizes = [
    (256, 256),
    (512, 512),
    (1024, 1024),
    (1280, 1280),
    (1920, 1920),
    (2160, 2160),
    (2560, 2560),
    (2880, 2880),
    (3200, 3200)
]

# Data storage list
results = []

print("Starting latency breakdown test with varying input sizes...")

for width, height in image_sizes:
    # Build the image URL from Picsum with the current size
    image_url = f"https://picsum.photos/{width}/{height}"
    print(f"\nTesting with image size: {width}x{height}")

    # Loop over both platforms
    for platform, url in [("Azure", AZURE_FUNCTION_URL), ("OpenFaaS", OPENFAAS_FUNCTION_URL)]:
        start_time = time.time()
        try:
            response = requests.get(url, params={"url": image_url})
            elapsed_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                entry = {
                    "platform": platform,
                    "image_size": f"{width}x{height}",
                    "elapsed_time": round(elapsed_time, 2),
                    "overall_duration": data.get("overall_duration", None),
                    "network_duration": data.get("network_duration", None),
                    "cpu_duration": data.get("cpu_duration", None),
                    "ml_duration": data.get("ml_duration", None)
                }
                results.append(entry)
                print(f"{platform} ({width}x{height}): {entry}")
            else:
                print(f"{platform} ({width}x{height}): Failed with status {response.status_code}")
        except Exception as e:
            print(f"{platform} ({width}x{height}): Request failed - {e}")

# Save results to CSV file
csv_filename = "latency_breakdown_results.csv"
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["platform", "image_size", "elapsed_time", "overall_duration", "network_duration", "cpu_duration", "ml_duration"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {csv_filename}")
