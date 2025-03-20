# Evaluation of Python Runtimes on Commercial vs Open-source Serverless Platforms

## Overview

This repository contains the code, scripts, and documentation for my COMP5123M Cloud Computing Coursework 2. The coursework involves experimenting with commercial and open-source serverless platforms, implementing functions, analyzing performance, and documenting findings.  

## Repository Contents

- 📂 **Azure Functions/** – Contains all Azure function implementations.  
- 📂 **OpenFaas/** – Contains all OpenFaaS function implementations.  

## Research Report

### Q1: General Information

1) Commercial serverless platform: **Microsoft Azure Functions** 

   For my investigation, I chose Azure Functions as my commercial FaaS platform. I have previous experience using Azure Functions for my Distributed Systems coursework last year, which meant that I already had the necessary dependencies installed on my machine. This familiarity helped me get started quickly without spending additional time on setup. Azure Functions is also one of the most commonly evaluated FaaS platform in studies investigating runtime performance on serverless functions (Djemame et. al. 2022).

2) Open-source serverless platform: **OpenFaaS** 
   
   For my investigation, I chose OpenFaas as my open source FaaS platform, as I found the provided tutorial in the labs easy to understand and use. Additionally, I was able to set up the OpenFaaS server on the Azure VM with minimal complications.

3) Programming Language: **Python** 
   
   For my investigation, I chose Python as the language runtime. Python is widely used in serverless computing, with well-supported frameworks for Azure Functions and OpenFaaS (Balla et. al. . It is the primary language I use for machine learning and API development, making it a practical choice for implementing my function. I also wanted to implement a machine learning model for my workflow, and I have familiarity with the same in Python with popular AI/ML libraries like TensorFlow and scikit-learn.

4) Application description:
   My chosen application is a simple image classifier. It uses a MobileNetV2 model from Keras, pretrained on the ImageNet dataset, to process an image classification request. The function takes an image URL as input, downloads it, performs basic pre-processing, and then runs an ML-based classification model. It returns a structured JSON response with the top 3 predicted labels for the image along with their probabilities, and a breakdown of the latency across each type of task (network latency (time to fetch the image), CPU-bound computation time, and ML inference time).


### Q2: Problem Motivation and Related Work
Problem Motivation:
Cloud computing has transformed access to scalable compute power with its pay-as-you-go model. Serverless computing takes this further by removing the need for developers to manage infrastructure, instead allowing them to deploy code that runs in response to events. This model has gained traction for its ability to scale applications automatically, optimize resource allocation, and reduce operational complexity (Djemame et al.). Platforms like AWS Lambda, Microsoft Azure Functions, and Google Cloud Functions exemplify this approach, where execution is triggered as needed, and costs are based solely on actual usage. By eliminating the overhead of provisioning and maintaining servers, serverless computing streamlines development and enables rapid deployment of applications.

Several factors affect the efficiency and effectiveness of serverless functions, such as cold start latency, execution time, resource constraints, and scaling behavior. Cold start latency occurs when a function has not been invoked for a period of time, requiring the platform to allocate resources before execution can begin. This can introduce delays, particularly for languages like Python, which rely on interpreted runtimes (Jackson & Clynch, 2018). Execution time and throughput are also critical, as they impact cost efficiency and the ability to handle concurrent workloads. While commercial platforms like Azure Functions offer built-in auto-scaling, open-source alternatives like OpenFaaS provide greater control over resource allocation, potentially leading to differences in performance under varying conditions.

This experiment aims to comparatively evaluate the performance of two prominent serverless platforms—Azure Functions (a commercial platform) and OpenFaaS (an open-source platform)—for Python runtimes, using a simple image processing application. The experiment focuses on the capabilities and performance of the Python runtime, comparing metrics such as latency, throughput, and resource usage under varying load conditions.

Related Work:
To ensure a comprehensive understanding of the topic, my experiment builds on research from prior studies like Djemame et. al. (2022), which evaluate the performance of language runtimes in open source serverless platforms. Djemame, et. al (2022) discusses the concept of the cold-start latency problem, and how existing literature focuses mainly on commercial FaaS platforms such as Microsoft Azure and Amazon Web Services (AWS), with a gap in research on open-source serverless platforms, which is one of Djemame et. al. (2022)’s main research questions. This highlights the importance of my experiment comparing commercial and open-source platforms. 

Jackson and Clynch (2018), cited in Djemame et. al. (2022), studied cold start overheads in different FaaS environments, and found that cold start times vary significantly across different FaaS platforms. In their experiments, they also follows other cited work to identify ideal testing intervals for measuring the cold start latency. Their work highlighted that interpreted languages (like Python) suffer from higher cold start delays compared to other compiled languages. 

Baldini et al. (2017), as cited in Djemame et. al. (2022), explains how an investigation comparing different FaaS platforms is important for developers, as understanding the various merits and demerits of each platform is essential to make the best choice of architectures for an application, and avoid vendor-specific lock in. They also outline various factors of the FaaS model that negatively affect performance of serverless applications, such as the cold-start problem. As cited in Djemame et. al. (2022), they along with Lloyd et. al. (2018) also analyzed the auto-scaling mechanisms of different FaaS providers, noting that commercial platforms like AWS Lambda and Azure Functions offer more robust scaling compared to open-source solutions.

Balla et. al (2020) in their paper “Open source faas performance aspects” discuss popularity of Python on serverless platforms, and the OpenFaaS architecture including it’s scale-to-zero functionality. Their experimental design using OpenFaaS’s built-in auto-scaling feature and load testing configurations were useful for me to implement my own experimental design.

Ataie et. al. (2025) also performed similar experiments with similar configurations to Balla et. al. (2020), but disabled autoscaling for their OpenFaaS functions. Their results concluded that Python is the best language runtime for the OpenFaaS open source serverless platform.

These studies provide useful insights into the current research in runtime performance for serverless environments, providing context for my work, as I aim to compare cold start behavior, runtime performance, and scaling behavior between Azure Functions and OpenFaaS when executing an ML workload. By extending their work, I aim to investigate the runtime performance of Python on both commercial and open-source platforms, offering insights into the trade-offs between these two platforms.

References:
1.	Djemame, K., Datsev, D., & Kelefouras, V. (2022). Evaluation of language runtimes in open-source serverless platforms. Proceedings of the 12th International Conference on Cloud Computing and Services Science, 123-132. Available from: https://eprints.whiterose.ac.uk/186083/
2.	Baldini, I., Castro, P., Chang, K., Cheng, P., Fink, S., Ishakian, V., Mitchell, N., Muthusamy, V., Rabbah, R., Slominski, A., and Suter, P. (2017). Serverless computing: Current trends and open problems. CoRR,abs/1706.03178.
3.	Lloyd, W., Ramesh, S., Chinthalapati, S., Ly, L., and Pallickara, S. (2018). Serverless computing: An investigation of factors influencing microservice performance. In 2018 IEEE International Conference on Cloud Engineering (IC2E), pages 159–169.
4.	Azure (2021). Azure functions. https://docs.microsoft.com/en-us/azure/azurefunctions/.
5.	OpenFaaS (2021). Openfaas - serverless functions, made simple. https://openfaas.com/.
6.	Jackson, D. and Clynch, G. (2018). An investigation of the impact of language runtime on the performance and cost of serverless functions. In 2018 IEEE/ACM International Conference on Utility and Cloud Computing Companion, pages 154–160.
7.	Ataie, E., Pooshani, M. and Aqasizade, H., An Empirical Study on the Impact of Programming Languages on the Performance of Open-source Serverless Platforms.
8.	Balla, D., Maliosz, M. and Simon, C., 2020, July. Open source faas performance aspects. In 2020 43rd International Conference on Telecommunications and Signal Processing (TSP) (pp. 358-364). IEEE.

### Q3: Experimental Design and Implementation - Commercial
Function Design: 
My Azure Functions app vin-image-processing-workflow deploys an HTTP-triggered Azure Function process-image, written in Python with the v2 programming model. The function uses a pre-trained Keras MobileNetV2 model to classify images provided the image URL, and returns the top 3 classes predicted.  The function was first developed and tested locally using VSCode before being deployed on the Azure cloud under the Consumption Plan. I used Python 3.11.9 to maintain compatibility with Azure’s runtime. 

To evaluate the function’s scalability and performance, I conducted load testing using Locust, simulating concurrent users and measuring throughput, latency, and failure rates under different load conditions.

To analyze the function's cold start performance, I wrote a custom Python script (measure_cold_start.py) that implements an exponential backoff strategy. This script invokes the function at increasing intervals to determine the delay introduced when the function instance is not pre-warmed. Additionally, I developed another script to analyze how input image size impacts latency, breaking down response times into network delay, CPU processing, and ML inference time.

For testing, I made use of the Lorem Picsum API to serve random images of a consistent size, ensuring consistency in input size and an easy way to source images. This ensured that input variability did not affect performance results.

Experiment Implementation: 
Load Testing: Once the function was deployed on the Azure cloud and ready to be tested, to evaluate the function’s scalability and performance, I conducted load testing using Locust, simulating concurrent users and measuring throughput, latency, and failure rates under different load conditions. I did a number of experiments with various numbers of total users and concurrent requests to evaluate average response times, throughput, and failure rates. First, a single user test o establish a baseline for function performance under minimal load, then 100 concurrent users (2 spawn rate) where users were added gradually to observe how the function scales under a steady increase in load, and 100 concurrent users (10 spawn rate) where users were added rapidly, testing Azure’s ability to handle sudden traffic spikes. The reports generated by Locust for the same are in azure_report_1users_spawn1.html, azure_report_100users_spawn2.html and azure_report_100users_spawn10.html respectively.

Cold Start Analysis: To analyze the function's cold start performance, I wrote a custom Python script (measure_cold_start.py) that implements an exponential backoff strategy. This script invokes the function at increasing intervals to determine the delay introduced when the function instance is not pre-warmed. Using the measure_cold_start.py script, I triggered the function after exponentially increasing idle periods (e.g., 1 min, 2 min, 4 min, etc.) to identify the minimum wait time required for a cold start, upto a maximum idle period of 32 minutes. The results of the same are in the Results section. 

Latency Breakdown: Additionally, I developed another script to analyze how input image size impacts latency, breaking down response times into network delay, CPU processing, and ML inference time. Varying the input size, I used the JSON metrics returned by my function to analyze the relative contributions of network, CPU processing, and ML inference time to the overall latency, and how this varies with input size. The results of the same are saved in latency_breakdown_results.csv and are in the Results section. 

### Q4: Experimental Design and Implementation - Open Source
Function Design: 
My Azure Functions app vin-image-processing-workflow deploys an HTTP-triggered Azure Function process-image, written in Python with the v2 programming model. The function uses a pre-trained Keras MobileNetV2 model to classify images provided the image URL, and returns the top 3 classes predicted.  The function was first developed and tested locally using VSCode before being deployed on the Azure cloud under the Consumption Plan. I used Python 3.11.9 to maintain compatibility with Azure’s runtime. 

To evaluate the function’s scalability and performance, I conducted load testing using Locust, simulating concurrent users and measuring throughput, latency, and failure rates under different load conditions.

To analyze the function's cold start performance, I wrote a custom Python script (measure_cold_start.py) that implements an exponential backoff strategy. This script invokes the function at increasing intervals to determine the delay introduced when the function instance is not pre-warmed. Additionally, I developed another script to analyze how input image size impacts latency, breaking down response times into network delay, CPU processing, and ML inference time.

For testing, I made use of the Lorem Picsum API to serve random images of a consistent size, ensuring consistency in input size and an easy way to source images. This ensured that input variability did not affect performance results.

Experiment Implementation: 
Load Testing: Once the function was deployed on my OpenFaaS faasd on my Azure VM, and ready to be tested, to evaluate the function’s scalability and performance, I conducted load testing using Locust, simulating concurrent users and measuring throughput, latency, and failure rates under different load conditions. I did a number of experiments with various numbers of total users and concurrent requests to evaluate average response times, throughput, and failure rates. First, a single user test o establish a baseline for function performance under minimal load, then 100 concurrent users (2 spawn rate) where users were added gradually to observe how the function scales under a steady increase in load, and 100 concurrent users (10 spawn rate) where users were added rapidly, testing OpenFaaS’s ability to handle sudden traffic spikes. The reports generated by Locust for the same are in openfaas_report_1users_spawn1.html, openfaas_report_100users_spawn2.html and openfaas_report_100users_spawn10.html respectively.

Cold Start Analysis: To analyze the function's cold start performance, I wrote a custom Python script (measure_cold_start.py) that implements an exponential backoff strategy. This script invokes the function at increasing intervals to determine the delay introduced when the function instance is not pre-warmed. Using the measure_cold_start.py script, I triggered the function after exponentially increasing idle periods (e.g., 1 min, 2 min, 4 min, etc.) to identify the minimum wait time required for a cold start, upto a maximum idle period of 32 minutes. The results of the same are in the Results section. 

Latency Breakdown: Additionally, I developed another script to analyze how input image size impacts latency, breaking down response times into network delay, CPU processing, and ML inference time. Varying the input size, I used the JSON metrics returned by my function to analyze the relative contributions of network, CPU processing, and ML inference time to the overall latency, and how this varies with input size. The results of the same are saved in latency_breakdown_results.csv and are in the Results section.

### Q5: Results and Evaluation
Load Testing results: 
Key metrics analyzed include average response time, request failures, and requests per second (RPS) across three test scenarios: 1 user (1 spawn), 100 users (2 spawns), and 100 users (10 spawns).

- Azure Performance:
o	1 User, 1 Spawn: Avg Response Time: 589.73ms, Min / Max Response Time: 214ms / 19,066ms, Total Requests: 83, Failures: 0, Requests per Second (RPS): 0.28. Azure handled a single request well, though the maximum response time peaked significantly at 19s, indicating occasional outliers in performance.

o	100 Users, 2 Spawns: Avg Response Time: 542.39ms, Min / Max Response Time: 176ms / 22,220ms, Total Requests: 7,747, Failures: 1, RPS: 25.87. Despite a higher load, Azure maintained an average response time under 600ms, with only one request failure. However, the maximum latency increased significantly to 22s, suggesting that under peak load, some requests experience much longer delays.

o	100 Users, 10 Spawns: Avg Response Time: 777.8ms, Min / Max Response Time: 172ms / 27,851ms, Total Requests: 7,866, Failures: 0, RPS: 26.27. The average response time increased by ~43% (from 542.39ms to 777.8ms) with more concurrent users, showing the effect of scaling constraints. The maximum response time peaked at 27.8s, further indicating that Azure experiences significant latency spikes under high load.

- OpenFaaS Performance
o	1 User, 1 Spawn: Avg Response Time: 335.31ms, Min / Max Response Time: 234ms / 443ms, Total Requests: 89, Failures: 0, RPS: 0.3. OpenFaaS outperformed Azure in this test, achieving an average response time ~43% lower than Azure (335ms vs. 590ms) and a significantly lower max response time (443ms vs. 19s on Azure).

o	100 Users, 2 Spawns: Avg Response Time: 7,298.74ms, Min / Max Response Time: 256ms / 12,951ms, Total Requests: 2,635, Failures: 0, RPS: 8.8. OpenFaaS struggled significantly with higher concurrency, with average latency increasing to 7.3s (compared to 542ms on Azure). This suggests that the platform experiences delays in function execution under load.

o	100 Users, 10 Spawns: Avg Response Time: 7,527.85ms, Min / Max Response Time: 490ms / 9,939ms, Total Requests: 2,761, Failures: 0, RPS: 9.22. The response times remained consistently high (~7.5s), with minimal improvement despite a higher request rate. The maximum response time slightly decreased compared to the 100-user, 2-spawn test, but overall performance remained significantly slower than Azure under high loads.

Therefore the results conclude that OpenFaaS consistently outperformed Azure in single-user scenarios, with a 43% lower average response time and a significantly lower max response time. On the other hand, Azure scaled better, with response times increasing from ~540ms to ~770ms under high load, while OpenFaaS struggled significantly, reaching 7.3–7.5s response times, making it ~10x slower than Azure at high concurrency. Neither platform had significant failures, indicating good reliability. However, Azure had one failure at 100 users, 2 spawns, while OpenFaaS had zero failures throughout.

•	Cold Start results: 
Cold start times varied significantly between the commercial platform (Azure) and the open-source OpenFaaS (faasd) environment. The results indicate that OpenFaaS consistently exhibited very minute, if any, cold start delays, while Azure experienced a clear, large spikes in latency due to cold start. At the initial call (cold state), Azure had a total duration of 18.53s, while OpenFaaS completed in 1.79s. When next called after 1 minutes, Azure’s overall execution duration dropped significantly to 1.07s, whereas OpenFaaS performed even faster at 0.57s, demonstrating they are both still warm from the previous call. 

As wait time between calls increased to 2-4 minutes, both platforms stabilized, with OpenFaaS maintaining an average total duration of 0.57s compared to Azure’s fluctuating durations (ranging from 0.72s to 1.14s). When called after 8 minutes, Azure experienced a cold start spike, reaching 19.5s, while OpenFaaS maintained a near-instantaneous response of 0.37s. Therefore, the time after which a function is not kept warm in Azure is between 4-8 minutes. 

Beyond 8 minutes, for calls after 16-32 minutes Azure cold started every time, and execution time ranged between 19–22s, while OpenFaaS remained under 0.6s, highlighting its superior ability to keep functions readily available. These results suggest that OpenFaaS (faasd) mitigates cold starts more effectively than Azure, likely due to differences in containerization and resource allocation strategies.

•	Latency Breakdown results: 
The overall latency, network duration and CPU duration increase with image size for both Azure and OpenFaaS, and this is clearer in the attached graphs as well (overall_duration_vs_image_size.png, network_duration_vs_image_size.png, cpu_duration_vs_image_size.png). Azure Functions has better CPU duration and is roughly similar to OpenFaaS on the network and overall durations. The ML duration tends to vary irregularly, but this also could be due to the actual image and how similar it is to the ImageNet dataset the model was trained on and so is not reliably a function of input size alone. 

For small image sizes (256x256 to 1024x1024), OpenFaaS consistently outperformed Azure in overall duration, processing images ~30–50% faster. For medium image sizes (1280x1280 to 1920x1920), both platforms demonstrated increased latency, with OpenFaaS still maintaining a lower overall duration. For 1920x1920, OpenFaaS had a higher latency spike (0.97s) compared to Azure (0.20s), which may indicate bottlenecks at this resolution. For images up to 2560x2560, OpenFaaS remained faster, but the performance gap narrowed. At 2880x2880, both platforms performed similarly (1.42s on Azure, 1.47s on OpenFaaS). At 3200x3200, OpenFaaS had a slightly higher total latency (1.67s vs. 1.56s on Azure).

These results suggest that OpenFaaS maintains a performance advantage in small to medium workloads but experiences increased overhead at larger image sizes. This could be attributed to resource constraints or differences in how the platforms allocate compute power for function execution.

This experiment provides insights into the performance characteristics of Azure Functions and OpenFaaS under varying loads and provide a deeper understanding of the performance trade-offs between commercial and open-source serverless platforms. By focusing on a single language runtime (Python) and common functionality in the functions, the experiment allows for a focused and fair comparison, ensuring that any differences in performance are attributed to the platforms rather than the language or application itself. 

### Q6: Code/Scripts

Link to Git Repository: [GitHub Repository](https://github.com/Vindhyaa-Saravanan/CloudComputingCoursework2)

### Q7: Demo Video [Demo Video](https://youtube.com/yourdemo)  
A short video demonstrating the deployment process, function execution, and performance results.


