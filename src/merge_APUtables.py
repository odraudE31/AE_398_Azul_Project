import pandas as pd
from pathlib import Path

# Define the project base directory (auto-detection)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the input file path
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

# Load Excel file
xls = pd.ExcelFile(INPUT_FILE)

# Read sheets
apu_report_state = xls.parse('APUReportState')
apu_last_start = xls.parse('APULastStart')

# Standardize column names
apu_report_state.columns = apu_report_state.columns.str.lower()
apu_last_start.columns = apu_last_start.columns.str.lower()

# Merge datasets on shared keys only
merged_df = pd.merge(
    apu_report_state,
    apu_last_start,
    how='inner',
    on=['flightid', 'equipmentregistration', 'departurestation']
)

# Save merged results as Parquet
parquet_output_path = BASE_DIR / "data/APUAnalysis.parquet"
merged_df.to_parquet(parquet_output_path, index=False)

print(f"✅ Merged data saved to Parquet: {parquet_output_path}")
