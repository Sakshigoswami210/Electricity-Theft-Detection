import pandas as pd
from pathlib import Path

data_folder = Path("data/raw/residential_data")

files = sorted(data_folder.glob("*.csv"))

summary = []

for file in files:
    df = pd.read_csv(file)

    df["Datetime"] = pd.to_datetime(df["TS"], unit="s")

    summary.append({
        "Meter_ID": file.stem,
        "Records": len(df),
        "Start_Date": df["Datetime"].min(),
        "End_Date": df["Datetime"].max(),
        "Days_Covered": (df["Datetime"].max() - df["Datetime"].min()).days,
        "Missing_Values": df.isnull().sum().sum()
    })

summary_df = pd.DataFrame(summary)

summary_df["Meter_ID"] = summary_df["Meter_ID"].astype(int)

summary_df = summary_df.sort_values("Meter_ID")

print(summary_df.to_string(index=False))

print("\nTotal records across all meters:", summary_df["Records"].sum())

print("\nRecords statistics:")
print(summary_df["Records"].describe())