import pandas as pd
from sklearn.ensemble import IsolationForest

input_file = "data/processed/ml_ready_data.csv"
output_file = "data/processed/anomaly_results.csv"

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

X = df[features]

model = IsolationForest(
    n_estimators=200,
    contamination="auto",
    random_state=42,
    n_jobs=-1
)

model.fit(X)

df["Anomaly_Score"] = -model.decision_function(X)

df["Anomaly_Flag"] = model.predict(X)

df["Anomaly_Flag"] = df["Anomaly_Flag"].map({
    1: 0,
    -1: 1
})

df.to_csv(output_file, index=False)

print("Isolation Forest model trained successfully.")
print("Total records:", len(df))
print("Anomalies detected:", df["Anomaly_Flag"].sum())
print(
    "Anomaly percentage:",
    round(df["Anomaly_Flag"].mean() * 100, 2),
    "%"
)

print("\nAnomaly score statistics:")
print(df["Anomaly_Score"].describe())