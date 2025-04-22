import pandas as pd
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
    if 'APUReportState' not in xls.sheet_names:
        print("Sheet 'APUReportState' not found in the Excel file.")
        return
    
    df = xls.parse('APUReportState')
    
    # Check if the necessary columns exist
    if 'TransitStartUTC' not in df.columns or 'TransitEndUTC' not in df.columns:
        print("Columns 'TransitStartUTC' or 'TransitEndUTC' not found in the sheet.")
        return
    
    # Convert columns to datetime
    df['TransitStartUTC'] = pd.to_datetime(df['TransitStartUTC'], errors='coerce')
    df['TransitEndUTC'] = pd.to_datetime(df['TransitEndUTC'], errors='coerce')
    
    # Remove invalid values
    df = df.dropna(subset=['TransitStartUTC', 'TransitEndUTC'])
    
    # Calculate elapsed time in seconds
    df['ElapsedSeconds'] = (df['TransitEndUTC'] - df['TransitStartUTC']).dt.total_seconds()
    
    # Remove negative values (in case of data errors)
    df = df[df['ElapsedSeconds'] >= 0]
    
    if df.empty:
        print("No valid elapsed time data available.")
        return
    
    # Calculate statistics
    avg_time = df['ElapsedSeconds'].mean()
    mode_time = df['ElapsedSeconds'].mode().iloc[0] if not df['ElapsedSeconds'].mode().empty else None
    min_time = df['ElapsedSeconds'].min()
    max_time = df['ElapsedSeconds'].max()
    
    # Display results
    print(f"Average elapsed time: {format_time(avg_time)}")
    print(f"Mode of elapsed time: {format_time(mode_time) if mode_time is not None else 'N/A'}")
    print(f"Shortest elapsed time: {format_time(min_time)}")
    print(f"Longest elapsed time: {format_time(max_time)}")
    
    # Plot histogram of elapsed times
    plt.figure(figsize=(10, 5))
    plt.hist(df['ElapsedSeconds'] / 3600, bins=30, edgecolor='black', alpha=0.7)  # Convert seconds to hours
    plt.xlabel("Elapsed Time (Hours)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Flight Durations")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Example usage
calculate_time_statistics(INPUT_FILE)
