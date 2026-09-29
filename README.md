# Python File Automation Toolkit

A collection of Python utilities for automating repetitive business tasks involving files and operational data.

## Current project: CSV Customer Report Processor

This project processes customer CSV reports by:

- Loading multiple CSV files.
- Validating required columns.
- Handling invalid or unreadable files.
- Merging valid datasets.
- Removing duplicate customers.
- Exporting the cleaned data to a CSV file.

## Technologies

- Python 3
- Pandas
- pathlib
- pytest
- Git
- CSV

## Project structure

```text
python-file-automation-toolkit/
├── data/
│   ├── input/
│   └── output/
├── src/
│   └── merge_csv_reports.py
├── tests/
│   └── test_merge_csv_reports.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3
- pip

## Installation

Clone the repository and create a virtual environment:
```bash
git clone https://github.com/josemaria-espejo/python-file-automation-toolkit.git
cd python-file-automation-toolkit

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Place the CSV files to be processed in:

`data/input/`

Run the script with:
```bash
python src/merge_csv_reports.py
```
The processed file will be generated in:

`data/output/merged_customers.csv`

When duplicate customers are found, the last occurrence is kept based on the sorted input-file order.

## Testing

Run the test suite with:

```bash
python -m pytest
```
The project includes unit tests for CSV loading, validation, merging, duplicate removal and exporting, as well as an end-to-end workflow test.

## Future development

The toolkit will gradually be expanded with additional automation utilities for business and operational data processing.