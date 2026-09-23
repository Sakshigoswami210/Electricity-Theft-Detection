import pandas as pd

input_file = "data/processed/meter_anomaly_results.csv"

df = pd.read_csv(input_file)

print("Anomaly score statistics:")
print(df["Anomaly_Score"].describe())

print("\nAnomaly score percentiles:")

percentiles = [0.90, 0.95, 0.97, 0.98, 0.99, 0.995, 0.999]

for p in percentiles:
    value = df["Anomaly_Score"].quantile(p)
    print(f"{p * 100}%: {value:.6f}")