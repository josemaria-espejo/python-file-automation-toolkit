import pandas as pd

from src.merge_csv_reports import remove_duplicate_customer


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