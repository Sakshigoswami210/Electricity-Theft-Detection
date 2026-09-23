import pandas as pd

file_path = "data/processed/combined_meter_data.csv"

df = pd.read_csv(file_path)

df["Datetime"] = pd.to_datetime(df["Datetime"])

df = df.sort_values(["Meter_ID", "Datetime"])

df["Time_Gap"] = df.groupby("Meter_ID")["Datetime"].diff()

large_gaps = df[df["Time_Gap"] > pd.Timedelta(hours=1)].copy()

large_gaps["Missing_Hours"] = (
    large_gaps["Time_Gap"].dt.total_seconds() / 3600
) - 1

print("Total records:", len(df))

print("\nNumber of gap events:", len(large_gaps))

print(
    "\nTotal missing hourly slots:",
    int(large_gaps["Missing_Hours"].sum())
)

print(
    "\nLargest missing period:",
    large_gaps["Time_Gap"].max()
)

print("\nMissing hours by Meter:")

missing_by_meter = (
    large_gaps.groupby("Meter_ID")["Missing_Hours"]
    .sum()
    .reset_index()
)

missing_by_meter["Missing_Hours"] = (
    missing_by_meter["Missing_Hours"].round().astype(int)
)

print(missing_by_meter.to_string(index=False))