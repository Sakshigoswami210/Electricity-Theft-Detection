import pandas as pd

file_path = "data/raw/residential_data/1.csv"

df = pd.read_csv(file_path)

df["Datetime"] = pd.to_datetime(df["TS"], unit="s")

df["Time_Gap"] = df["Datetime"].diff()

print("Total records:", len(df))

print("\nTime gap distribution:")
print(df["Time_Gap"].value_counts().sort_index())

print("\nGaps greater than 1 hour:")

large_gaps = df[df["Time_Gap"] > pd.Timedelta(hours=1)][
    ["Datetime", "Time_Gap"]
]

print(large_gaps.to_string(index=False))

print("\nNumber of large gaps:", len(large_gaps))