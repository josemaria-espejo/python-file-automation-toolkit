from pathlib import Path
import pandas as pd

INPUT_FOLDER = Path("data/input")
OUTPUT_FOLDER = Path("data/output")

csv_files = list(INPUT_FOLDER.glob("*.csv"))

print(f"Found {len(csv_files)} CSV files in {INPUT_FOLDER}:")
for file in csv_files:
    print(f"- {file.name}")