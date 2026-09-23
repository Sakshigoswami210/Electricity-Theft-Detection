import pandas as pd

input_file = "data/processed/meter_data_features.csv"

df = pd.read_csv(input_file)

print("Dataset shape:")
print(df.shape)

print("\nConsumption statistics:")
print(
    df["Total_Consumption_Wh"].describe()
)

print("\nVoltage statistics:")

voltage_columns = [
    "V1",
    "V2",
    "V3",
    "Average_Voltage_V"
]

print(
    df[voltage_columns].describe()
)

print("\nConsumption percentiles:")

print(
    df["Total_Consumption_Wh"].quantile(
        [0.50, 0.75, 0.90, 0.95, 0.99, 0.999]
    )
)

print("\nZero consumption records:")

print(
    (df["Total_Consumption_Wh"] == 0).sum()
)

print("\nMeters:")
print(df["Meter_ID"].nunique())

print("\nConsumption by meter:")

meter_summary = (
    df.groupby("Meter_ID")["Total_Consumption_Wh"]
    .agg(["count", "mean", "median", "std", "max"])
)

print(meter_summary.to_string())