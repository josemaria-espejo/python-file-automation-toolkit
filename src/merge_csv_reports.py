from pathlib import Path
import pandas as pd

INPUT_FOLDER = Path("data/input")
OUTPUT_FOLDER = Path("data/output")

REQUIRED_COLUMNS = {
    "id", 
    "name", 
    "identity_number"
}


def load_csv_files(csv_files):
    """Read all CSV files and return a list of DataFrames."""

    customer_dataframes = []
    invalid_files = {}

    for file in csv_files:
        print(f"Reading '{file.name}'...")

        customer_data = pd.read_csv(file)

        missing_columns = validate_dataframe(customer_data)
        if missing_columns:
            invalid_files[file.name] = missing_columns
            continue

        customer_dataframes.append(customer_data)

    return customer_dataframes, invalid_files

def validate_dataframe(dataframe):
    """Validate that the DataFrame contains the required columns."""

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    return missing_columns


def merge_data(customer_dataframes):
    """Merge a list of Dataframes into a single DataFrame."""

    merged_data = pd.concat(customer_dataframes, ignore_index=True)

    return merged_data


def remove_duplicate_customer(merged_data):
    """Remove duplicate rows based on the 'identity_number' column."""

    cleaned_data = merged_data.drop_duplicates(subset = ["identity_number"], keep = "last")

    return cleaned_data

def export_data(cleaned_data):
    """Export the cleaned DataFrame to a CSV file."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_FOLDER / "merged_customers.csv"
    cleaned_data.to_csv(output_file, index=False)

    print(f"\nSuccessfully exported cleaned data to: '{output_file}'.")


def main():

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

    customer_dataframes, invalid_files = load_csv_files(csv_files)

    if invalid_files:
        print("\nFiles that failed validation:")
        for file_name, missing_columns in invalid_files.items():
            missing_columns_text=", ".join(sorted(missing_columns))
            print(f"- {file_name} -> "
                f"Missing required columns: {missing_columns_text}")

    if not customer_dataframes:
        print("\nERROR: No valid CSV files could be processed.")
        exit()
        
    total_rows = sum(len(dataframe) for dataframe in customer_dataframes)
    print(f"\nSuccessfully loaded {total_rows} rows.")

    # 3. Merge data.

    merged_data = merge_data(customer_dataframes)

    # 4. Remove duplicates.

    rows_before = len(merged_data)
    print(f"\nRows before removing duplicates: {rows_before}")

    cleaned_data = remove_duplicate_customer(merged_data)

    rows_after = len(cleaned_data)
    duplicates_removed = rows_before - rows_after

    # 5. Display results.
    print(f"Rows after removing duplicates: {rows_after}")
    print(f"Duplicates removed: {duplicates_removed}")

    print("\nMerged customer data:")
    print(f"\n{cleaned_data}\n")

    # 6. Export cleaned data to CSV.
    export_data(cleaned_data)


if __name__ == "__main__":
    main()
