import pandas as pd
import numpy as np

input_file = "data/processed/meter_data_features.csv"
output_file = "data/processed/ml_ready_data.csv"

df = pd.read_csv(input_file)

features = [
    "Total_Consumption_Wh",
    "Average_Voltage_V",
    "Previous_Consumption_Wh",
    "Consumption_Change_Wh",
    "Rolling_24h_Mean",
    "Rolling_24h_Std",
    "Consumption_Deviation",
    "Rolling_Z_Score",
    "Hour",
    "Day_of_Week",
    "Is_Weekend"
]

ml_df = df[
    ["Meter_ID", "Datetime"] + features
].copy()

ml_df = ml_df.replace([np.inf, -np.inf], np.nan)

before = len(ml_df)

ml_df = ml_df.dropna(subset=features).reset_index(drop=True)

after = len(ml_df)

ml_df.to_csv(output_file, index=False)

print("ML-ready dataset created successfully.")
print("Rows before cleaning:", before)
print("Rows after cleaning:", after)
print("Rows removed:", before - after)
print("Final shape:", ml_df.shape)

print("\nRemaining missing values:")
print(ml_df[features].isna().sum())

print("\nInfinite values:", np.isinf(ml_df[features]).sum().sum())