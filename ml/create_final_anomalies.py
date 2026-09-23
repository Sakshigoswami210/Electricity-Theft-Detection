import pandas as pd

input_file = "data/processed/meter_anomaly_results.csv"
output_file = "data/processed/final_anomaly_results.csv"
threshold_file = "data/processed/meter_thresholds.csv"

df = pd.read_csv(input_file)

MIN_RECORDS = 100
PERCENTILE = 0.99

results = []
thresholds = []

for meter_id, meter_data in df.groupby("Meter_ID"):
    meter_data = meter_data.copy()

    record_count = len(meter_data)

    if record_count < MIN_RECORDS:
        meter_data["Final_Anomaly_Flag"] = 0

        thresholds.append({
            "Meter_ID": meter_id,
            "Records": record_count,
            "Threshold": None,
            "Status": "Insufficient records"
        })

    else:
        threshold = meter_data["Anomaly_Score"].quantile(PERCENTILE)

        meter_data["Final_Anomaly_Flag"] = (
            meter_data["Anomaly_Score"] >= threshold
        ).astype(int)

        thresholds.append({
            "Meter_ID": meter_id,
            "Records": record_count,
            "Threshold": threshold,
            "Status": "Eligible"
        })

    results.append(meter_data)

final_df = pd.concat(results, ignore_index=True)

threshold_df = pd.DataFrame(thresholds)

final_df.to_csv(output_file, index=False)
threshold_df.to_csv(threshold_file, index=False)

print("Final anomaly detection completed.")
print("Total records:", len(final_df))
print(
    "Final anomaly candidates:",
    final_df["Final_Anomaly_Flag"].sum()
)

print(
    "Overall candidate percentage:",
    round(
        final_df["Final_Anomaly_Flag"].mean() * 100,
        2
    ),
    "%"
)

print("\nAnomaly candidates by meter:")

summary = (
    final_df.groupby("Meter_ID")
    .agg(
        Total_Records=("Meter_ID", "size"),
        Candidates=("Final_Anomaly_Flag", "sum")
    )
)

summary["Candidate_Percentage"] = (
    summary["Candidates"]
    / summary["Total_Records"]
    * 100
)

print(summary.to_string())

print("\nThreshold information:")
print(threshold_df.to_string(index=False))