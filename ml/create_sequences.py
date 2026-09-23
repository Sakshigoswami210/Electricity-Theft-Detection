import pandas as pd

input_file = "data/processed/combined_meter_data.csv"
output_file = "data/processed/meter_data_with_sequences.csv"

df = pd.read_csv(input_file)

df["Datetime"] = pd.to_datetime(df["Datetime"])

df = df.sort_values(["Meter_ID", "Datetime"]).reset_index(drop=True)

df["Time_Gap"] = df.groupby("Meter_ID")["Datetime"].diff()

df["New_Sequence"] = (
    df["Time_Gap"].isna()
    | (df["Time_Gap"] > pd.Timedelta(hours=1))
)

df["Sequence_ID"] = (
    df.groupby("Meter_ID")["New_Sequence"]
    .cumsum()
)

df.to_csv(output_file, index=False)

print("Sequence dataset created successfully.")

print("\nShape:")
print(df.shape)

print("\nNumber of meters:")
print(df["Meter_ID"].nunique())

print("\nTotal sequences:")
print(df.groupby("Meter_ID")["Sequence_ID"].nunique().sum())

print("\nExample:")
print(
    df[
        [
            "Meter_ID",
            "Datetime",
            "Time_Gap",
            "Sequence_ID"
        ]
    ].head(20).to_string(index=False)
)

print("\nOutput file:")
print(output_file)