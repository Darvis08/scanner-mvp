# app.py

from fastapi import FastAPI
from bse_scraper import fetch_bse_announcements
from event_detector import detect_risk_event
from risk_engine import calculate_riskscore
from historical_scraper import fetch_bse_historical_announcements
import json
import os

app = FastAPI()

# Load Historical Data (if exists)
if os.path.exists('historical_events.json'):
    with open('historical_events.json', 'r') as f:
        historical_events_data = json.load(f)
else:
    historical_events_data = {}

@app.get("/")
def root():
    return {"message": "Scanner MVP API is running"}

@app.get("/fetch-historical")
def fetch_historical_data():
    try:
        fetch_bse_historical_announcements()
        return {"message": "Historical data fetched and saved successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/scan")
def scan_companies():
    # Live fetch today's announcements
    announcements = fetch_bse_announcements()

    company_events = {}

    # Load live events detected today
    for announcement in announcements:
        company = announcement["company"]
        subject = announcement["subject"]
        date = announcement["date"]

        event_type = detect_risk_event(subject)
        if event_type:
            if company not in company_events:
                company_events[company] = []
            company_events[company].append({
                "event": event_type,
                "date": date
            })

    # Merge historical events if available
    for company, hist_events in historical_events_data.items():
        if company not in company_events:
            company_events[company] = []
        company_events[company].extend(hist_events)

    # Now calculate RiskScore
    results = []
    for company, events in company_events.items():
        riskscore, band = calculate_riskscore(events)
        results.append({
            "company": company,
            "riskscore": riskscore,
            "band": band,
            "events": events
        })

    results = sorted(results, key=lambda x: x["riskscore"], reverse=True)

    return {"results": results}
