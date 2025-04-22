import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

# Define the project base directory (auto-detection)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define the input file path
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

def calculate_time_statistics(file_path):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Check if the sheet exists
    if 'APUAnalysis' not in xls.sheet_names:
        print("Sheet 'APUAnalysis' not found in the Excel file.")
        return
    
    df = xls.parse('APUAnalysis')
    
    # Check if the necessary columns exist
    if 'apuuseminute_y' not in df.columns:
        print("Column 'apuuseminute_y' not found in the sheet.")
        return
    
    # Remove invalid values
    df = df.dropna(subset=['apuuseminute_y'])
    
    # Remove negative values (in case of data errors)
    df = df[df['apuuseminute_y'] >= 0]
    
    if df.empty:
        print("No valid elapsed time data available.")
        return
    
    # Calculate statistics
    avg_time = df['apuuseminute_y'].mean()
    mode_time = df['apuuseminute_y'].mode().iloc[0] if not df['apuuseminute_y'].mode().empty else None
    min_time = df['apuuseminute_y'].min()
    max_time = df['apuuseminute_y'].max()
    
    # Display results
    print(f"Average elapsed time: {avg_time}")
    print(f"Mode of elapsed time: {mode_time if mode_time is not None else 'N/A'}")
    print(f"Shortest elapsed time: {min_time}")
    print(f"Longest elapsed time: {max_time}")

    # Plot histogram of elapsed times in minutes
    plt.figure(figsize=(10, 5))
    plt.hist(df['apuuseminute_y'], bins=range(0, 61), edgecolor='black', alpha=0.7)
    plt.xlabel("APU Use (Minutes)")
    plt.ylabel("Frequency")
    plt.title("Distribution of APU Usage Duration (0–60 min)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Limit x-axis to 0–60 and show each minute
    plt.xticks(np.arange(0, 61, 2))
    plt.xlim(0, 60)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(BASE_DIR / "graphs/apu_usage_histogram.png", dpi=600, bbox_inches='tight')

    plt.show()


# Example usage
calculate_time_statistics(INPUT_FILE)
