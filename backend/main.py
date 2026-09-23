from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI(
    title="Electricity Theft Detection API",
    description="API for electricity consumption anomaly detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://localhost:27017/")

db = client["electricity_theft_db"]
collection = db["anomaly_events"]


@app.get("/")
def root():
    return {"message": "Electricity Theft Detection API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/anomalies")
def get_anomalies():
    events = list(collection.find({}, {"_id": 0}))

    return {
        "total_events": len(events),
        "events": events
    }


@app.get("/anomalies/{meter_id}")
def get_meter_anomalies(meter_id: int):
    events = list(
        collection.find(
            {"Meter_ID": meter_id},
            {"_id": 0}
        )
    )

    return {
        "meter_id": meter_id,
        "total_events": len(events),
        "events": events
    }


@app.get("/meter-readings/{meter_id}")
def get_meter_readings(meter_id: int):
    readings = list(
        db["meter_readings"].find(
            {"Meter_ID": meter_id},
            {"_id": 0}
        )
    )

    return {
        "meter_id": meter_id,
        "total_readings": len(readings),
        "readings": readings
    }