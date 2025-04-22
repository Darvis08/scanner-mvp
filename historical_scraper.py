# historical_scraper.py

import requests
import json
import time
import random
from fo_companies import fo_companies
from event_detector import detect_risk_event

def fetch_bse_historical_announcements():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    historical_events = {}

    for company in fo_companies:
        historical_events[company] = []
        for year in range(2019, 2025):  # From 2019 to 2024
            try:
                # Very basic simulation because BSE API is restricted without key
                # In real version: Use browser automation (Playwright) to scrape
                search_url = f"https://api.bseindia.com/BseIndiaAPI/api/Announce/GetData?strCat=-1&strPrevDate={year}-01-01&strScrip=&strSearch={company.replace(' ', '%20')}&strToDate={year}-12-31"

                response = requests.get(search_url, headers=headers)
                data = response.json()

                if 'Table' in data:
                    for ann in data['Table']:
                        subject = ann.get('NEWS_SUBJECT', '')
                        announce_date = ann.get('NEWS_DT', '')

                        event_type = detect_risk_event(subject)
                        if event_type and announce_date:
                            historical_events[company].append({
                                "event": event_type,
                                "date": announce_date
                            })

                time.sleep(random.uniform(1.0, 2.0))  # polite to server
            except Exception as e:
                print(f"Error fetching {company} for {year}: {e}")

    # Save all into a file
    with open('historical_events.json', 'w') as f:
        json.dump(historical_events, f, indent=2)

    return historical_events

# To run manually
if __name__ == "__main__":
    fetch_bse_historical_announcements()
