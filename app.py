# app.py
from fastapi import FastAPI
from scraper import fetch_latest_announcements
from risk_engine import calculate_riskscore

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Scanner MVP API is running"}

@app.get("/scan")
def scan_companies():
    results = []
    data = fetch_latest_announcements()
    for entry in data:
        company = entry["company"]
        events = entry["events"]
        score, band = calculate_riskscore(events)
        results.append({
            "company": company,
            "events": events,
            "riskscore": score,
            "band": band
        })
    return {"results": results}
