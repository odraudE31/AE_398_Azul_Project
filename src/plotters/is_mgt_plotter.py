import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the base directory and Parquet file path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PARQUET_FILE = BASE_DIR / "data/D0D14.parquet"

def analyze_is_mgt_column(file_path):
    # Load the Parquet file
    try:
        df = pd.read_parquet(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Check if the 'IS_MGT' column exists
    if 'IS_MGT' not in df.columns:
        print("Column 'IS_MGT' not found in the file.")
        return

    # Count frequency including NaN
    counts = df['IS_MGT'].value_counts(dropna=False)

    # Replace NaN with 'NULL' for clarity in labels
    counts.index = [str(i) if pd.notna(i) else "NULL" for i in counts.index]

    print("📊 Frequency of values in the 'IS_MGT' column:")
    for value, count in counts.items():
        print(f"  {value}: {count}")

    # Plot the distribution
    plt.figure(figsize=(6, 4))
    counts.plot(kind='bar', color='cornflowerblue', edgecolor='black')
    plt.title("Distribution of IS_MGT Values")
    plt.xlabel("IS_MGT (0 = < MGT, 1 = ≥ MGT, NULL = unknown)")
    plt.ylabel("Frequency")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot
    output_path = BASE_DIR / "graphs/is_mgt_distribution.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=600, bbox_inches='tight')

    plt.show()

# Run the analysis
analyze_is_mgt_column(PARQUET_FILE)
