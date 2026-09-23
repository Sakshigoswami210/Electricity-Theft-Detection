import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/processed/meter_data_features.csv"
df = pd.read_csv(input_file)

hourly_consumption = df.groupby("Hour")["Total_Consumption_Wh"].mean()

plt.figure(figsize=(10, 6))
plt.plot(hourly_consumption.index, hourly_consumption.values, marker="o")
plt.xlabel("Hour of Day")
plt.ylabel("Average Consumption (Wh)")
plt.title("Average Electricity Consumption by Hour")
plt.xticks(range(24))
plt.grid(True)
plt.tight_layout()
plt.savefig("screenshots/hourly_consumption.png", dpi=150)
plt.show()