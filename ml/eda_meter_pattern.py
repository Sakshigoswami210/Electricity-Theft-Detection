import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/processed/meter_data_features.csv"
df = pd.read_csv(input_file)

meter_consumption = (
    df.groupby("Meter_ID")["Total_Consumption_Wh"]
    .mean()
    .sort_values()
)

plt.figure(figsize=(12, 6))
plt.bar(meter_consumption.index.astype(str), meter_consumption.values)
plt.xlabel("Meter ID")
plt.ylabel("Average Consumption (Wh)")
plt.title("Average Electricity Consumption by Meter")
plt.tight_layout()
plt.savefig("screenshots/meter_consumption.png", dpi=150)
plt.show()