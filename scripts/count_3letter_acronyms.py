import pandas as pd
from collections import Counter

def count_departure_acronyms(file_path):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Load the specific sheet
    if 'APULastStart' not in xls.sheet_names:
        print("Sheet 'APULastStart' not found in the Excel file.")
        return
    
    df = xls.parse('APULastStart')
    
    # Check if the column 'DepartureStation' exists
    if 'DepartureStation' not in df.columns:
        print("Column 'DepartureStation' not found in the sheet.")
        return
    
    # Extract the 'DepartureStation' column and count occurrences of unique three-letter acronyms
    acronyms = df['DepartureStation'].dropna().astype(str).str.strip()
    counter = Counter(acronyms)
    
    # Print the results
    for acronym, count in counter.items():
        print(f"{acronym}: {count}")

# Example usage
count_departure_acronyms("DataSample.xlsx")
 