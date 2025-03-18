from locust import HttpUser, task, between

class OpenFaaSUser(HttpUser):
    host = "http://20.26.125.107:8080"
    wait_time = between(1, 5)

    @task
    def process_image(self):
        self.client.get("/function/process-image?url=https://picsum.photos/700/800", name="/openfaas/process-image")

class AzureFunctionUser(HttpUser):
    host = "https://vin-image-processing-workflow.azurewebsites.net"
    wait_time = between(1, 5)

    @task
    def classify_image(self):
        self.client.get("/api/classify_image?url=https://picsum.photos/700/800", name="/azure/classify_image")
