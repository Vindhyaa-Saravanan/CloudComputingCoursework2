# MEASURE_COLD_START.PY
# Python script with performance test for detecting cold starts in Azure Functions and OpenFaaS.             
#
# Name of Student: Vindhyaa Saravanan
# Module: Cloud Computing Systems
# Student ID: 201542641
# Username: sc21vs

# This script performs exponential backoff to detect cold starts in Azure Functions and OpenFaaS.
# It sends requests to both platforms at increasing intervals and compares the response times to detect cold starts.
# The results are saved to a CSV file for analysis.

import requests
import time
import csv
import json

# Function URLs
AZURE_FUNCTION_URL = "https://vin-image-processing-workflow.azurewebsites.net/api/classify_image"
OPENFAAS_FUNCTION_URL = "http://20.26.125.107:8080/function/process-image"
IMAGE_URL = "https://picsum.photos/400/500"

# Initial waiting interval time (in seconds) before retrying (exponential backoff)
initial_wait_time = 60  # Start at interval size of 1 min
max_wait_time = 1920  # Test intervals upto 32 minutes long

# Data storage
results = []

print("Starting cold start detection...")

# Do initial call to then start exponential backoff
print(f"First call to functions before starting exponential search...")
for platform, url in [("Azure", AZURE_FUNCTION_URL), ("OpenFaaS", OPENFAAS_FUNCTION_URL)]:
        initial_start_time = time.time()
        
        try:
            response = requests.get(url, params={"url": IMAGE_URL})
            initial_elapsed_time = time.time() - initial_start_time

            if response.status_code == 200:
                result = response.json()
                entry = {
                    "platform": platform,
                    "wait_time": 0,
                    "elapsed_time": initial_elapsed_time,   
                    "total_duration": result["overall_duration"],
                    "network_duration": result["network_duration"],
                    "cpu_duration": result["cpu_duration"],
                    "ml_duration": result["ml_duration"],
                }
                results.append(entry)
                print(f"{platform}: {entry}")

            else:
                print(f"{platform}: Failed with status {response.status_code}")

        except Exception as e:
            print(f"{platform}: Request failed - {e}")

wait_time = initial_wait_time
while wait_time <= max_wait_time:
    print(f"\nWaiting {wait_time // 60} minutes before calling function...")

    time.sleep(wait_time)

    for platform, url in [("Azure", AZURE_FUNCTION_URL), ("OpenFaaS", OPENFAAS_FUNCTION_URL)]:
        start_time = time.time()
        
        try:
            response = requests.get(url, params={"url": IMAGE_URL})
            elapsed_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                entry = {
                    "platform": platform,
                    "wait_time": wait_time,
                    "elapsed_time": elapsed_time,   
                    "total_duration": result["overall_duration"],
                    "network_duration": result["network_duration"],
                    "cpu_duration": result["cpu_duration"],
                    "ml_duration": result["ml_duration"],
                }
                results.append(entry)
                print(f"{platform}: {entry}")

            else:
                print(f"{platform}: Failed with status {response.status_code}")

        except Exception as e:
            print(f"{platform}: Request failed - {e}")

    # Increase wait time exponentially
    wait_time *= 2  

# Save results to CSV
csv_filename = "cold_start_times.csv"
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["platform", "wait_time", "elapsed_time", "total_duration", "network_duration", "cpu_duration", "ml_duration"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {csv_filename}")
