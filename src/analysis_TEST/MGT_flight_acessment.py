import pandas as pd
import numpy as np
from pathlib import Path

# Define the project base directory and input file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "data/D0D14.parquet"

# Load Parquet file
d0d14 = pd.read_parquet(INPUT_FILE)

# Aircraft MGT dictionary
aircrafts = {
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
        return np.nan  # usa NaN para manter tipo numérico
    elif planned_ground_time >= mgt:
        return 1
    elif planned_ground_time < mgt:
        return 0

# Apply the function to add the new column 'IS_MGT'
d0d14['IS_MGT'] = d0d14.apply(is_mgt, axis=1)

# Save modified DataFrame to Parquet file
d0d14.to_parquet(INPUT_FILE, index=False)

print("✅ 'IS_MGT' added to the Parquet file.")
