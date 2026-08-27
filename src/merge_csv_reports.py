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
    """Read and validate CSV files, returning valid DataFrames and errors."""

    customer_dataframes = []
    invalid_files = {}
    read_errors = {}

    for file in csv_files:
        print(f"Reading '{file.name}'...")

        try:
            customer_data = pd.read_csv(file)
        except pd.errors.ParserError as error:
            read_errors[file.name] = {
                "type": "ParserError",
                "message": str(error)
            }
            continue
        except UnicodeDecodeError as error:
            read_errors[file.name] = {
                "type": "UnicodeDecodeError",
                "message": str(error)
            }
            continue
        
        missing_columns = validate_dataframe(customer_data)
        if missing_columns:
            invalid_files[file.name] = missing_columns
            continue

        customer_dataframes.append(customer_data)

    return customer_dataframes, invalid_files, read_errors

def validate_dataframe(dataframe):
    """Validate that the DataFrame contains the required columns."""

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    return missing_columns


def merge_data(customer_dataframes):
    """Merge a list of DataFrames into a single DataFrame."""

    if not customer_dataframes:
        raise ValueError("At least one DataFrame is required to merge data.")
    
    merged_data = pd.concat(customer_dataframes, ignore_index=True)

    return merged_data


def remove_duplicate_customer(merged_data):
    """Remove duplicate rows based on the 'identity_number' column."""

    cleaned_data = merged_data.drop_duplicates(subset = ["identity_number"], keep = "last")

    return cleaned_data

def export_data(cleaned_data, output_folder):
    """Export the cleaned DataFrame to a CSV file."""

    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "merged_customers.csv"
    cleaned_data.to_csv(output_file, index=False)

    return output_file


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

    customer_dataframes, invalid_files, read_errors = load_csv_files(csv_files)

    if invalid_files:
        print("\nFiles that failed validation:")
        for file_name, missing_columns in invalid_files.items():
            missing_columns_text=", ".join(sorted(missing_columns))
            print(f"- {file_name} -> "
                f"Missing required columns: {missing_columns_text}")

    if read_errors:
        print("\nFiles that couldn't be read:")
        for file_name, error in read_errors.items():
            if error["type"] == "ParserError":
                error_description = "Could not parse CSV structure."
            elif error["type"] == "UnicodeDecodeError":
                error_description = "Could not decode file encoding."
            else:
                error_description = "Unknown read error."

            print(
                f"- {file_name} -> "
                f"{error_description} "
                f"Error: {error['message']}"
            )

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
    output_file = export_data(cleaned_data, OUTPUT_FOLDER)
    print(f"\nSuccessfully exported cleaned data to: '{output_file}'.")


if __name__ == "__main__":
    main()
