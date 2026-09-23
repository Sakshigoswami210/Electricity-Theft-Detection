import pandas as pd
from pymongo import MongoClient

CSV_FILE = "data/processed/final_anomaly_results.csv"

client = MongoClient("mongodb://localhost:27017/")

db = client["electricity_theft_db"]
collection = db["meter_readings"]

df = pd.read_csv(CSV_FILE)

columns = [
    "Meter_ID",
    "Datetime",
    "Total_Consumption_Wh",
    "Average_Voltage_V",
    "Consumption_Change_Wh",
    "Rolling_24h_Mean",
    "Rolling_24h_Std",
    "Consumption_Deviation",
    "Hour",
    "Day_of_Week",
    "Is_Weekend",
    "Anomaly_Score",
    "Final_Anomaly_Flag"
]

df = df[columns]

records = df.to_dict(orient="records")

collection.delete_many({})

if records:
    collection.insert_many(records)

collection.create_index([("Meter_ID", 1), ("Datetime", 1)])

print("Meter readings loaded successfully!")
print("Records inserted:", collection.count_documents({}))

client.close()