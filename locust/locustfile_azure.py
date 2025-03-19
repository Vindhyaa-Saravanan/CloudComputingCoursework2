# LOCUSTFILE.PY
# Python file with Locust load testing script for Coursework 2.                  
#
# Name of Student: Vindhyaa Saravanan
# Module: Cloud Computing Systems
# Student ID: 201542641
# Username: sc21vs

# Following is the MIT License for Locust:
# 
# The MIT License

# Copyright (c) 2009-2025, Carl Byström, Jonatan Heyman, Lars Holmberg

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from locust import HttpUser, task, between

class AzureFunctionUser(HttpUser):
    host = "https://vin-image-processing-workflow.azurewebsites.net"
    wait_time = between(1, 5)

    @task
    def classify_image(self):
        self.client.get("/api/classify_image?url=https://picsum.photos/700/800", name="/azure/classify_image")
