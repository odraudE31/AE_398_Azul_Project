import pandas as pd
from pathlib import Path

# Define the project base directory (auto-detect)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define paths relative to the project root
INPUT_FILE = BASE_DIR / "data/DataSample.xlsx"

# Load the Excel file
xls = pd.ExcelFile(INPUT_FILE)

# Load the desired sheet
df = xls.parse('D0D14')

# Check the data types of the columns before modifying them
print("Original data types:")
print(df.dtypes)

# Define the desired columns
columns = ['FLIGHT_KEY_UTC', 'FLIGHT_NUMBER', 'SCHEDULED_FLEET', 'LATEST_FLEET', 'ACFT_REGISTRATION', 
           'AIRPORT_LATEST_DEPARTURE', 'AIRPORT_SCHEDULED_ARRIVAL', 'SCHEDULED_DEPARTURE_UTC_DTIME', 
           'ACTUAL_DEPARTURE_UTC_DTIME', 'TAXI_OUT_REALIZED', 'DELAY_DEPARTURE_MIN', 'D0', 'D14', 
           'GROUNDTIME_STANDARD_MIN', 'GROUNDTIME_PLANNED_MIN', 'GROUNDTIME_REALIZED_MIN', 'GROUNDTIME_ADHERENCE']

# Ensure that the columns are present in the file
df = df[columns]

# Handle categorical columns (convert to string) and numerical columns separately
df['SCHEDULED_FLEET'] = df['SCHEDULED_FLEET'].fillna('Unknown').astype(str)

# For numerical columns, fill NaN values with 0 or another suitable value
numerical_columns = ['DELAY_DEPARTURE_MIN', 'D0', 'D14', 'GROUNDTIME_STANDARD_MIN', 
                     'GROUNDTIME_PLANNED_MIN', 'GROUNDTIME_REALIZED_MIN', 'GROUNDTIME_ADHERENCE']

df[numerical_columns] = df[numerical_columns].fillna(0)  # Fill NaN values with 0 for numerical columns

# Check the data types of the columns after the conversion
print("\nData types after conversion:")
print(df.dtypes)

# Save the DataFrame as a Parquet file
OUTPUT_FILE = BASE_DIR / "data/D0D14.parquet"  
df.to_parquet(OUTPUT_FILE, engine='pyarrow')

print(f'Parquet file saved at: {OUTPUT_FILE}')
