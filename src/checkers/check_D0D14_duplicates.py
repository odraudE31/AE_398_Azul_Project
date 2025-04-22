import pandas as pd
from pathlib import Path

# Load the D0D14.parquet file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "data/D0D14.parquet"
df_d0d14 = pd.read_parquet(INPUT_FILE)

# --- Standardize column names ---
df_d0d14.columns = df_d0d14.columns.str.upper()

# --- Count occurrences of each FLIGHT_KEY_UTC ---
flight_key_counts = df_d0d14['FLIGHT_KEY_UTC'].value_counts()

# --- Filter to only FLIGHT_KEY_UTC values that appear 2 or more times ---
duplicates = flight_key_counts[flight_key_counts >= 2]

# --- Print out the duplicate FLIGHT_KEY_UTC values with their counts ---
print("Duplicate FLIGHT_KEY_UTC values in D0D14:")
for flight_key, count in duplicates.items():
    print(f"FLIGHT_KEY_UTC: {flight_key} appears {count} times")

# --- Print the total number of duplicated FLIGHT_KEY_UTC values ---
print("\nTotal number of FLIGHT_KEY_UTC entries with duplicates:", len(duplicates))
