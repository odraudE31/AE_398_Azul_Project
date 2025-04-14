import pandas as pd
from pathlib import Path

# Define the project base directory (auto-detection)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the input file path
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

# Load Excel file
file_path = BASE_DIR / "data/DataSample.xlsx"
xls = pd.ExcelFile(file_path)

# Read sheets
apu_report_state = xls.parse('APUReportState')
apu_last_start = xls.parse('APULastStart')

# Standardize column names
apu_report_state.columns = apu_report_state.columns.str.lower()
apu_last_start.columns = apu_last_start.columns.str.lower()

# Merge datasets on shared keys
merged_df = pd.merge(
    apu_report_state,
    apu_last_start,
    how='inner',
    on=['flightid', 'equipmentregistration', 'departurestation']
)

# Convert time columns to datetime
merged_df['transitstartutc'] = pd.to_datetime(merged_df['transitstartutc'])
merged_df['transitendutc'] = pd.to_datetime(merged_df['transitendutc'])
merged_df['apulaststart'] = pd.to_datetime(merged_df['apulaststart'])

# Calculate turnaround and APU timing metrics
merged_df['ground_time_min'] = (merged_df['transitendutc'] - merged_df['transitstartutc']).dt.total_seconds() / 60
merged_df['apu_on_before_pushback_min'] = (merged_df['transitendutc'] - merged_df['apulaststart']).dt.total_seconds() / 60

# Flag compliance with APU 5-min rule
merged_df['apu_5min_compliant'] = merged_df['apu_on_before_pushback_min'].between(4, 6)

# Save to a new sheet in the same Excel file
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    merged_df.to_excel(writer, sheet_name='APUAnalysis', index=False)

print("✅ Merged results saved to 'APUAnalysis' sheet.")
