import pandas as pd

input_file = "data/processed/anomaly_results.csv"
output_file = "data/processed/top_anomalies.csv"

df = pd.read_csv(input_file)

top_anomalies = (
    df.sort_values("Anomaly_Score", ascending=False)
    .head(100)
)

columns = [
    "Meter_ID",
    "Datetime",
    "Total_Consumption_Wh",
    "Previous_Consumption_Wh",
    "Consumption_Change_Wh",
    "Rolling_24h_Mean",
    "Rolling_24h_Std",
    "Consumption_Deviation",
    "Rolling_Z_Score",
    "Hour",
    "Day_of_Week",
    "Anomaly_Score",
    "Anomaly_Flag"
]

top_anomalies[columns].to_csv(
    output_file,
    index=False
)

print("Top anomalies extracted successfully.")
print("Top 10 anomalies:")
print(top_anomalies[columns].head(10).to_string(index=False))
