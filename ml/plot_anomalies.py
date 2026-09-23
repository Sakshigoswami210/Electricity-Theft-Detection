import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/processed/final_anomaly_results.csv"

df = pd.read_csv(input_file)
df["Datetime"] = pd.to_datetime(df["Datetime"])

meter_id = 36

meter_data = (
    df[df["Meter_ID"] == meter_id]
    .sort_values("Datetime")
)

normal = meter_data[
    meter_data["Final_Anomaly_Flag"] == 0
]

anomalies = meter_data[
    meter_data["Final_Anomaly_Flag"] == 1
]

plt.figure(figsize=(14, 6))

plt.plot(
    meter_data["Datetime"],
    meter_data["Total_Consumption_Wh"],
    label="Consumption"
)

plt.scatter(
    anomalies["Datetime"],
    anomalies["Total_Consumption_Wh"],
    label="Anomaly Candidate"
)

plt.xlabel("Date")
plt.ylabel("Consumption (Wh)")
plt.title(f"Consumption and Anomaly Candidates - Meter {meter_id}")
plt.legend()
plt.tight_layout()

plt.savefig(
    "screenshots/meter_36_anomalies.png",
    dpi=150
)

plt.show()