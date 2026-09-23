import pandas as pd

input_file = "data/processed/final_anomaly_results.csv"
output_file = "data/processed/anomaly_events.csv"

df = pd.read_csv(input_file)

df["Datetime"] = pd.to_datetime(df["Datetime"])

df = df.sort_values(
    ["Meter_ID", "Datetime"]
).reset_index(drop=True)

df["Time_Gap"] = (
    df.groupby("Meter_ID")["Datetime"]
    .diff()
)

df["Previous_Anomaly"] = (
    df.groupby("Meter_ID")["Final_Anomaly_Flag"]
    .shift(1)
)

new_group = (
    (df["Final_Anomaly_Flag"] == 1)
    & (
        (df["Previous_Anomaly"] != 1)
        | (df["Time_Gap"] > pd.Timedelta(hours=1))
    )
)

df["Anomaly_Group"] = (
    new_group
    .groupby(df["Meter_ID"])
    .cumsum()
)

anomalies = df[
    df["Final_Anomaly_Flag"] == 1
].copy()

events = (
    anomalies.groupby(
        ["Meter_ID", "Anomaly_Group"]
    )
    .agg(
        Start_Time=("Datetime", "min"),
        End_Time=("Datetime", "max"),
        Number_of_Anomalies=("Final_Anomaly_Flag", "size"),
        Maximum_Consumption_Wh=("Total_Consumption_Wh", "max"),
        Maximum_Anomaly_Score=("Anomaly_Score", "max"),
        Maximum_Deviation_Wh=("Consumption_Deviation", "max")
    )
    .reset_index()
)

events["Duration_Hours"] = (
    (
        events["End_Time"]
        - events["Start_Time"]
    ).dt.total_seconds()
    / 3600
) 

events["Investigation_Priority"] = "Review"

events = events.sort_values(
    ["Maximum_Anomaly_Score", "Number_of_Anomalies"],
    ascending=[False, False]
).reset_index(drop=True)

events.to_csv(
    output_file,
    index=False
)

print("Anomaly events created successfully.")
print("Total anomaly events:", len(events))

print("\nEvent columns:")
print(events.columns.tolist())

print("\nTop 20 anomaly events:")
print(events.head(20).to_string(index=False))