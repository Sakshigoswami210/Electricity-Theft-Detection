import pandas as pd
from sklearn.ensemble import IsolationForest

input_file = "data/processed/ml_ready_data.csv"
output_file = "data/processed/meter_anomaly_results.csv"

df = pd.read_csv(input_file)

features = [
    "Consumption_Change_Wh",
    "Consumption_Deviation",
    "Rolling_24h_Std",
    "Average_Voltage_V",
    "Hour",
    "Day_of_Week",
    "Is_Weekend"
]

results = []

for meter_id, meter_data in df.groupby("Meter_ID"):
    meter_data = meter_data.copy()

    X = meter_data[features]

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)

    meter_data["Anomaly_Score"] = -model.decision_function(X)

    meter_data["Anomaly_Flag"] = model.predict(X)

    meter_data["Anomaly_Flag"] = meter_data["Anomaly_Flag"].map({
        1: 0,
        -1: 1
    })

    results.append(meter_data)

results_df = pd.concat(results, ignore_index=True)

results_df.to_csv(output_file, index=False)

print("Meter-specific Isolation Forest models trained successfully.")
print("Total records:", len(results_df))
print("Total anomalies:", results_df["Anomaly_Flag"].sum())

print(
    "Overall anomaly percentage:",
    round(results_df["Anomaly_Flag"].mean() * 100, 2),
    "%"
)

print("\nAnomalies by meter:")

meter_summary = (
    results_df.groupby("Meter_ID")
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

print(meter_summary.to_string())