import pandas as pd
import pytest

from src.merge_csv_reports import (
    remove_duplicate_customer,
    validate_dataframe,
    merge_data,
    export_data
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
    