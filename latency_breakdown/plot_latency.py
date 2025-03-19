import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data
df = pd.read_csv('latency_breakdown_results.csv')

# Extract the width (assuming images are square, e.g., "256x256") as a numeric value
def extract_width(size_str):
    try:
        return int(size_str.split('x')[0])
    except Exception as e:
        return None

df['width'] = df['image_size'].apply(extract_width)

# List of measurement columns to plot
measurements = ['overall_duration', 'network_duration', 'cpu_duration', 'ml_duration']

# For each measurement, create a separate graph
for measure in measurements:
    plt.figure(figsize=(8, 6))
    
    # Filter data for each platform
    azure_df = df[df['platform'] == 'Azure']
    openfaas_df = df[df['platform'] == 'OpenFaaS']
    
    # Plot Azure results
    plt.plot(azure_df['width'], azure_df[measure], marker='o', linestyle='-', label='Azure Functions')
    # Plot OpenFaaS results
    plt.plot(openfaas_df['width'], openfaas_df[measure], marker='s', linestyle='-', label='OpenFaaS')
    
    plt.xlabel("Image Width (pixels)")
    plt.ylabel(f"{measure.replace('_', ' ').capitalize()} (seconds)")
    plt.title(f"{measure.replace('_', ' ').capitalize()} vs. Image Size")
    plt.legend()
    plt.grid(True)
    # Save the plot to a PNG file
    plt.savefig(f"{measure}_vs_image_size.png")
    plt.show()
