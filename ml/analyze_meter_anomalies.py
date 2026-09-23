import pandas as pd

input_file = "data/processed/anomaly_results.csv"

df = pd.read_csv(input_file)

meter_summary = (
    df.groupby("Meter_ID")
    .agg(
        Total_Records=("Meter_ID", "size"),
        Anomalies=("Anomaly_Flag", "sum")
    )
)

meter_summary["Anomaly_Percentage"] = (
    meter_summary["Anomalies"]
    / meter_summary["Total_Records"]
    * 100
)

meter_summary = meter_summary.sort_values(
    "Anomaly_Percentage",
    ascending=False
)

print("Anomaly distribution by meter:")
print(meter_summary.to_string())

print("\nOverall anomaly percentage:")
print(
    round(
        df["Anomaly_Flag"].mean() * 100,
        2
    ),
    "%"
)