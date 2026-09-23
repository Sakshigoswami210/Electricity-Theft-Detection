import pandas as pd
import matplotlib.pyplot as plt

input_file = "data/processed/meter_data_features.csv"

df = pd.read_csv(input_file)

plt.figure(figsize=(10, 6))

plt.hist(
    df["Total_Consumption_Wh"],
    bins=100
)

plt.xlabel("Total Consumption (Wh)")
plt.ylabel("Number of Observations")
plt.title("Distribution of Total Electricity Consumption")

plt.tight_layout()

plt.savefig(
    "screenshots/consumption_distribution.png",
    dpi=150
)

plt.show()