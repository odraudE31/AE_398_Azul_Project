import pandas as pd
from pathlib import Path

# Define the project base directory and input file
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

# Load Excel file and read sheets
xls = pd.ExcelFile(INPUT_FILE)

d0d14 = xls.parse('D0D14')

aircrafts = {
# aircraft : MGT
    'ATR': 30,
    'E1': 35,
    'E2': 40,
    'A320': 40,
    'A321': 50,
}    

def is_mgt(row):
    aircraft = row['LATEST_FLEET']
    planned_ground_time = row['GROUNDTIME_PLANNED_MIN']

    mgt = aircrafts.get(aircraft)
    if mgt is None:
        return 'NULL'
    elif planned_ground_time >= mgt:
        return 1
    elif planned_ground_time < mgt:
        return 0

# Apply function line by line
d0d14['IS_MGT'] = d0d14.apply(is_mgt, axis=1)

# Save modified D0D14 back to the Excel file
with pd.ExcelWriter(INPUT_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    d0d14.to_excel(writer, sheet_name='D0D14', index=False)

print("✅ 'nova_coluna' adicionada à planilha 'D0D14'.")
