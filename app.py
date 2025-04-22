# app.py (Upgraded to Real Data)

from fastapi import FastAPI
from bse_scraper import fetch_bse_announcements
from event_detector import detect_risk_event
from risk_engine import calculate_riskscore

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Scanner MVP API is running"}

@app.get("/scan")
def scan_companies():
    announcements = fetch_bse_announcements()
    company_events = {}

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

    results = []
    for company, events in company_events.items():
        riskscore, band = calculate_riskscore(events)
        results.append({
            "company": company,
            "riskscore": riskscore,
            "band": band,
            "events": events
        })

    # Sort by highest RiskScore first
    results = sorted(results, key=lambda x: x["riskscore"], reverse=True)

    return {"results": results}
