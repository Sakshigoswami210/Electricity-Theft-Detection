import pandas as pd

input_file = "data/processed/final_anomaly_results.csv"

df = pd.read_csv(input_file)

anomalies = df[
    df["Final_Anomaly_Flag"] == 1
].copy()

anomalies = anomalies.sort_values(
    "Anomaly_Score",
    ascending=False
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
    "Anomaly_Score"
]

print("Total anomaly candidates:", len(anomalies))

print("\nTop 20 anomaly candidates:")
print(
    anomalies[columns]
    .head(20)
    .to_string(index=False)
)

print("\nAnomaly candidates by meter:")
print(
    anomalies.groupby("Meter_ID")
    .size()
    .sort_values(ascending=False)
    .to_string()
)