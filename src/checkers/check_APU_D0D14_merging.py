import pandas as pd
from pathlib import Path
from collections import defaultdict

# Define the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

# Load Excel file
xls = pd.ExcelFile(INPUT_FILE)

# Read sheets
apu_report_state = xls.parse('APUReportState')
d0d14 = xls.parse('D0D14')

# Standardize column names
apu_report_state.columns = apu_report_state.columns.str.lower()
d0d14.columns = d0d14.columns.str.lower()

# Convert to datetime and numeric
apu_report_state['transitendutc'] = pd.to_datetime(apu_report_state['transitendutc'], errors='coerce')
d0d14['actual_departure_utc_dtime'] = pd.to_datetime(d0d14['actual_departure_utc_dtime'], errors='coerce')
d0d14['taxi_out_realized'] = pd.to_numeric(d0d14['taxi_out_realized'], errors='coerce')

# Calculate adjusted departure time
d0d14['adjusted_departure'] = d0d14['actual_departure_utc_dtime'] - pd.to_timedelta(d0d14['taxi_out_realized'], unit='m')

# Build lookup dictionary: registration -> list of adjusted departures
adjusted_times_dict = defaultdict(list)
for _, row in d0d14.iterrows():
    reg = row['acft_registration']
    adj_dep = row['adjusted_departure']
    if pd.notnull(reg) and pd.notnull(adj_dep):
        adjusted_times_dict[reg].append(adj_dep)

# Check for matches with optional tolerance
match_count = 0
total_checked = 0
tolerance = pd.Timedelta(minutes=5)

for _, row in apu_report_state.iterrows():
    reg = row['equipmentregistration']
    transit_end = row['transitendutc']
    if pd.notnull(reg) and pd.notnull(transit_end):
        total_checked += 1
        for adj_dep in adjusted_times_dict.get(reg, []):
            if abs(transit_end - adj_dep) <= tolerance:
                match_count += 1
                break  # Stop after first match

# Compute and display result
percentage_match = (match_count / total_checked) * 100 if total_checked > 0 else 0
print(f"✅ {percentage_match:.2f}% of APUReportState rows have a matching adjusted departure (±5 min) in D0D14.")
