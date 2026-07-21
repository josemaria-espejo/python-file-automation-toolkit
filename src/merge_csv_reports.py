from pathlib import Path
import pandas as pd

INPUT_FOLDER = Path("data/input")
OUTPUT_FOLDER = Path("data/output")


def load_csv_files(csv_files):
    """Read all CSV files and return a list of DataFrames."""

    customer_dataframes = []

    for file in csv_files:
        print(f"Reading '{file.name}'...")

        customer_data = pd.read_csv(file)

        customer_dataframes.append(customer_data)

    return customer_dataframes

def merge_data(customer_dataframes):
    """Merge a list of Dataframes into a single DataFrame."""

    merged_data = pd.concat(customer_dataframes, ignore_index=True)

    return merged_data


def remove_duplicates(merged_data):
    """Remove duplicate rows based on the 'identity_number' column."""

    cleaned_data = merged_data.drop_duplicates(subset = ["identity_number"], keep = "last")

    return cleaned_data

# 1.Discover input CSV files.

csv_files = list(INPUT_FOLDER.glob("*.csv"))

if not csv_files:
    print(f"No CSV files found in {INPUT_FOLDER}. Please add CSV files to the input folder and try again.")
    exit()

print(f"\nFound {len(csv_files)} CSV files in {INPUT_FOLDER}:")
for file in csv_files:
    print(f"- {file.name}")

# 2. Read CSV files.

print()

customer_dataframes = load_csv_files(csv_files)

total_rows = sum(len(dataframe) for dataframe in customer_dataframes)
print(f"\nSuccessfully loaded {total_rows} rows.")

# 3. Merge data.

merged_data = merge_data(customer_dataframes)

# 4. Remove duplicates.

rows_before = len(merged_data)
print(f"\nRows before removing duplicates: {rows_before}")

cleaned_data = remove_duplicates(merged_data)

rows_after = len(cleaned_data)
duplicates_removed = rows_before - rows_after

# 5. Display results.
print(f"Rows after removing duplicates: {rows_after}")
print(f"Duplicates removed: {duplicates_removed}")

print("\nMerged customer data:")
print(f"\n{cleaned_data}\n")


