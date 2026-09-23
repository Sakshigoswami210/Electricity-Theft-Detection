import pandas as pd
from pathlib import Path

data_folder = Path("data/raw/residential_data")
output_file = Path("data/processed/combined_meter_data.csv")

files = sorted(data_folder.glob("*.csv"), key=lambda x: int(x.stem))

all_data = []

for file in files:
    df = pd.read_csv(file)

    df["Meter_ID"] = int(file.stem)

    df["Datetime"] = pd.to_datetime(df["TS"], unit="s")

    df["Total_Consumption_Wh"] = df["W1"] + df["W2"] + df["W3"]

    df["Average_Voltage_V"] = (df["V1"] + df["V2"] + df["V3"]) / 3

    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

combined_df = combined_df[
    [
        "Meter_ID",
        "TS",
        "Datetime",
        "V1",
        "V2",
        "V3",
        "W1",
        "W2",
        "W3",
        "Total_Consumption_Wh",
        "Average_Voltage_V"
    ]
]

combined_df = combined_df.sort_values(
    ["Meter_ID", "Datetime"]
).reset_index(drop=True)

output_file.parent.mkdir(parents=True, exist_ok=True)

combined_df.to_csv(output_file, index=False)

print("Combined dataset created successfully.")

print("\nShape:")
print(combined_df.shape)

print("\nColumns:")
print(combined_df.columns.tolist())

print("\nMeters:")
print(combined_df["Meter_ID"].nunique())

print("\nMissing values:")
print(combined_df.isnull().sum())

print("\nFirst 5 rows:")
print(combined_df.head())

print("\nOutput file:")
print(output_file)
