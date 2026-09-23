import pandas as pd
import numpy as np

input_file = "data/processed/meter_data_with_sequences.csv"
output_file = "data/processed/meter_data_features.csv"

df = pd.read_csv(input_file)

df["Datetime"] = pd.to_datetime(df["Datetime"])

df = df.sort_values(
    ["Meter_ID", "Sequence_ID", "Datetime"]
).reset_index(drop=True)

group = df.groupby(["Meter_ID", "Sequence_ID"])

df["Previous_Consumption_Wh"] = (
    group["Total_Consumption_Wh"].shift(1)
)

df["Consumption_Change_Wh"] = (
    df["Total_Consumption_Wh"]
    - df["Previous_Consumption_Wh"]
)

df["Hour"] = df["Datetime"].dt.hour

df["Day_of_Week"] = df["Datetime"].dt.dayofweek

df["Is_Weekend"] = (
    df["Day_of_Week"] >= 5
).astype(int)

previous_consumption = (
    group["Total_Consumption_Wh"]
    .shift(1)
)

df["Rolling_24h_Mean"] = (
    previous_consumption
    .groupby([df["Meter_ID"], df["Sequence_ID"]])
    .rolling(window=24, min_periods=6)
    .mean()
    .reset_index(level=[0, 1], drop=True)
)

df["Rolling_24h_Std"] = (
    previous_consumption
    .groupby([df["Meter_ID"], df["Sequence_ID"]])
    .rolling(window=24, min_periods=6)
    .std()
    .reset_index(level=[0, 1], drop=True)
)

df["Consumption_Deviation"] = (
    df["Total_Consumption_Wh"]
    - df["Rolling_24h_Mean"]
)

df["Rolling_Z_Score"] = (
    df["Consumption_Deviation"]
    / df["Rolling_24h_Std"]
)

df.to_csv(output_file, index=False)

print("Feature dataset created successfully.")
print("Shape:", df.shape)

print("\nMissing values in new features:")
print(
    df[
        [
            "Previous_Consumption_Wh",
            "Consumption_Change_Wh",
            "Rolling_24h_Mean",
            "Rolling_24h_Std",
            "Consumption_Deviation",
            "Rolling_Z_Score"
        ]
    ].isna().sum()
)