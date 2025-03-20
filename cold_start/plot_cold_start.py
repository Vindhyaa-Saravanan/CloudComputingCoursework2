import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("cold_start_times.csv")

# Convert wait_time to minutes for better readability
df["wait_time_minutes"] = df["wait_time"] / 60

# Set seaborn style for better visuals
sns.set_theme(style="whitegrid")

# Function to plot comparisons
def plot_comparison(y_column, title, y_label, save_as):
    plt.figure(figsize=(8, 5))
    
    # Line plots for Azure and OpenFaaS
    sns.lineplot(data=df[df["platform"] == "Azure"], x="wait_time_minutes", y=y_column, label="Azure", marker="o")
    sns.lineplot(data=df[df["platform"] == "OpenFaaS"], x="wait_time_minutes", y=y_column, label="OpenFaaS", marker="s")
    
    plt.xlabel("Wait Time (minutes)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(save_as, dpi=300)  # Save figure
    plt.show()

# Generate plots
plot_comparison("elapsed_time", "Elapsed Time vs. Wait Time", "Elapsed Time (s)", "elapsed_time_vs_wait.png")
plot_comparison("total_duration", "Total Function Duration vs. Wait Time", "Total Duration (s)", "total_duration_vs_wait.png")
plot_comparison("network_duration", "Network Duration vs. Wait Time", "Network Duration (s)", "network_duration_vs_wait.png")
plot_comparison("cpu_duration", "CPU Duration vs. Wait Time", "CPU Duration (s)", "cpu_duration_vs_wait.png")
plot_comparison("ml_duration", "ML Processing Duration vs. Wait Time", "ML Duration (s)", "ml_duration_vs_wait.png")
