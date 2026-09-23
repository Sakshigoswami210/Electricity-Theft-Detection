# Electricity Theft Detection & Real-Time Monitoring System

## About the Project

This project is an end-to-end electricity consumption monitoring and anomaly detection system.

The main goal is to identify unusual electricity consumption patterns from smart meter data. I used historical residential electricity data and applied machine learning to detect consumption records that differ significantly from the normal behavior of individual meters.

The project includes data preprocessing, feature engineering, anomaly detection, a FastAPI backend, MongoDB database, React dashboard, and Power BI reporting.

> Note: An anomaly means unusual consumption behavior and does not directly confirm electricity theft.

---

## Features

- Electricity consumption data analysis
- Data cleaning and preprocessing
- Time-based and consumption-based feature engineering
- Anomaly detection using Isolation Forest
- Meter-specific anomaly detection
- Anomaly event grouping
- MongoDB data storage
- FastAPI REST API
- Interactive React dashboard
- Power BI dashboard
- Meter and date-based filtering
- Consumption and anomaly visualizations

---

## Tech Stack

**Programming & ML**
- Python
- Pandas
- NumPy
- Scikit-learn
- Isolation Forest

**Backend**
- FastAPI
- Uvicorn

**Database**
- MongoDB
- PyMongo

**Frontend**
- React
- TypeScript
- Vite
- Axios
- Recharts

**Visualization**
- Power BI

**Version Control**
- Git & GitHub

---

## Dataset

The project uses the Residential Data smart-meter dataset containing electricity measurements from residential apartments at IIT Bombay.

The original dataset contains:

- Timestamp
- Three-phase voltage measurements
- Three-phase electricity consumption measurements

Source:

https://figshare.com/s/a4aedbe2ae2aadc5618b

The consumption values from the three phases were combined to calculate total electricity consumption for each reading.

---

## How It Works

The project follows this pipeline:

```text
Smart Meter Data
       ↓
Data Cleaning & Preprocessing
       ↓
Feature Engineering
       ↓
Isolation Forest
       ↓
Meter-Specific Anomaly Detection
       ↓
Anomaly Thresholding
       ↓
Anomaly Event Generation
       ↓
MongoDB
       ↓
FastAPI
       ↓
React Dashboard
       ↓
Power BI Dashboard
Machine Learning

I used Isolation Forest for unsupervised anomaly detection.

Some of the features used by the model are:

Total Consumption
Consumption Change
Consumption Deviation
Rolling 24-hour Mean
Rolling 24-hour Standard Deviation
Average Voltage
Hour
Day of Week
Weekend Indicator

Separate models were used for individual meters because different meters can have very different normal consumption patterns.

A meter-specific threshold was then applied to identify the most unusual consumption records.

Results

The final processed dataset contains:

39 meters
180,799 scored records
1,827 anomaly candidates
1,422 anomaly events
Approximately 1.01% anomaly candidates

The detected anomalies represent unusual consumption patterns that may require further investigation. They are not treated as confirmed electricity theft cases.

Backend

The FastAPI backend provides APIs for accessing anomaly events and meter readings.

Main endpoints:

GET /
GET /health
GET /anomalies
GET /anomalies/{meter_id}
GET /meter-readings/{meter_id}

MongoDB is used to store the processed anomaly events and meter readings.

Database:

electricity_theft_db

Collections:

anomaly_events
meter_readings
React Dashboard

The React dashboard provides an interactive view of the detected anomalies and electricity consumption.

It includes:

Total anomaly events
Total energy consumption
Number of monitored meters
Anomaly events by meter
Consumption trend over time
Hourly consumption pattern
Anomaly events by hour
Meter filter
Date range filter

###Dashboard Preview
<img width="1297" height="736" alt="powerbi_dashboard" src="https://github.com/user-attachments/assets/0bf077fa-7aa7-411a-a606-a5965a1dd539" />


The frontend communicates with the FastAPI backend using Axios.

Power BI Dashboard

A Power BI dashboard was also created to analyze the processed data.

The dashboard includes:

Total Anomaly Events
Total Energy Consumption
Meters Monitored
Anomaly Events by Meter
Consumption Trend Over Time
Hourly Consumption Pattern
Anomaly Events by Hour
Meter and Date filters

The Power BI file is available in:

powerbi/Electricity_Theft_Detection_Dashboard.pbix
Project Structure
Energy-Theft-Detection Project/
│
├── backend/
├── data/
│   ├── raw/
│   └── processed/
├── frontend/
├── ml/
├── powerbi/
├── screenshots/
├── .gitignore
└── README.md
How to Run
Backend

Create and activate the virtual environment:

python -m venv venv

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install required packages:

pip install pandas numpy scikit-learn fastapi uvicorn pymongo

Start the FastAPI server:

uvicorn backend.main:app --reload

API documentation:

http://127.0.0.1:8000/docs
Frontend

Go to the frontend folder:

cd frontend

Install dependencies:

npm install

Start the React application:

npm run dev
Limitations
The project uses historical smart-meter data rather than live electricity-grid data.
Anomalies do not automatically mean electricity theft.
The dataset contains some missing periods and different amounts of data for different meters.
The model is unsupervised and does not use confirmed theft labels.
Future Improvements
Real-time smart-meter data integration
Automatic anomaly alerts
Email/SMS notifications
Cloud deployment
User authentication
Advanced anomaly detection models
Model monitoring and retraining
Author

Sakshi Goswami

Electronics & Telecommunication Engineering
