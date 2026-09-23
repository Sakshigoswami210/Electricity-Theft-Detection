import pandas as pd
from pymongo import MongoClient

CSV_FILE = "data/processed/anomaly_events.csv"

client = MongoClient("mongodb://localhost:27017/")

db = client["electricity_theft_db"]
collection = db["anomaly_events"]

df = pd.read_csv(CSV_FILE)

records = df.to_dict(orient="records")

collection.delete_many({})

if records:
    collection.insert_many(records)

print("MongoDB data insertion successful!")
print("Records inserted:", collection.count_documents({}))

client.close()