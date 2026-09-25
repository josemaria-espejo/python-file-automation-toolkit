import pandas as pd
import pytest

from src.merge_csv_reports import (
    remove_duplicate_customer,
    validate_dataframe,
    merge_data,
    export_data,
    load_csv_files
)

def test_remove_duplicate_customer():
    customer_data = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "name": ["Jose", "Ana", "Pedro", "Jose Updated"],
        "identity_number": [
            "12345678A",
            "23456789B",
            "34567890C",
            "12345678A"
        ]
    })

    cleaned_data = remove_duplicate_customer(customer_data)

    assert len(cleaned_data) == 3
    assert cleaned_data.iloc[-1]["name"] == "Jose Updated"

def test_validate_dataframe():
    valid_dataframe = pd.DataFrame({
        "id": [1, 2],
        "name": ["Jose", "Ana"],
        "identity_number": ["12345678A", "23456789B"]
    })

    missing_columns = validate_dataframe(valid_dataframe)
    assert missing_columns == set()

def test_validate_dataframe_with_missing_columns():
    invalid_dataframe = pd.DataFrame({
        "id": [1, 2],
        "name": ["Jose", "Ana"]
    })

    missing_columns = validate_dataframe(invalid_dataframe)
    assert missing_columns == {"identity_number"}

def test_merge_data():
    dataframe1 = pd.DataFrame({
        "id": [1, 2],
        "name": ["Jose", "Ana"],
        "identity_number": ["12345678A", "23456789B"]
    })

    dataframe2 = pd.DataFrame({
        "id": [3, 4],
        "name": ["Pedro", "Maria"],
        "identity_number": ["34567890C", "45678901D"]
    })

    expected_dataframe = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "name": ["Jose", "Ana", "Pedro", "Maria"],
        "identity_number": ["12345678A", "23456789B", "34567890C", "45678901D"]
    })

    merged_data = merge_data([dataframe1, dataframe2])
    assert expected_dataframe.equals(merged_data)

def test_merge_data_with_empty_list():
    with pytest.raises(
        ValueError, 
        match="At least one DataFrame is required to merge data."
    ):
        merge_data([])

def test_export_data(tmp_path): 
    customer_data = pd.DataFrame({
        "id": [1, 2],
        "name": ["Jose", "Ana"],
        "identity_number": ["12345678A", "23456789B"]
    })

    exported_file = export_data(customer_data, tmp_path)
    assert exported_file.exists()

    read_exported_data = pd.read_csv(exported_file)
    assert customer_data.equals(read_exported_data)

def test_load_csv_files_with_parser_error(tmp_path):
    malformed_csv = tmp_path / "malformed.csv"
    malformed_csv.write_text("""id,name,identity_number
    1,Jose,12345678A
    2,"Ana,23456789B
    3,Pedro,34567890C""")

    customer_dataframes, invalid_files, read_errors= load_csv_files([malformed_csv])
    assert len(customer_dataframes) == 0
    assert invalid_files == {}
    assert "malformed.csv" in read_errors
    assert read_errors["malformed.csv"]["type"] == "ParserError"

def test_load_csv_files_with_missing_columns(tmp_path):
    missing_columns_csv = tmp_path / "missing_columns.csv"
    missing_columns_csv.write_text("""id,name
    1,Jose
    2,Ana
    3,Pedro""")

    customer_dataframes, invalid_files, read_errors = load_csv_files([missing_columns_csv])
    assert len(customer_dataframes) == 0
    assert read_errors == {}
    assert "missing_columns.csv" in invalid_files
    assert invalid_files["missing_columns.csv"] == {"identity_number"}

def test_load_csv_files_with_valid_csv(tmp_path):
    valid_csv = tmp_path / "valid.csv"
    valid_csv.write_text("""id,name,identity_number
    1,Jose,12345678A
    2,Ana,23456789B
    3,Pedro,34567890C""")
    expected_dataframe = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Jose", "Ana", "Pedro"],
        "identity_number": ["12345678A", "23456789B", "34567890C"]
    })

    loaded_csvs, invalid_files, read_errors = load_csv_files([valid_csv])
    assert loaded_csvs[0].equals(expected_dataframe) == 1
    assert invalid_files == {}
    assert read_errors == {}
  

    
    


    