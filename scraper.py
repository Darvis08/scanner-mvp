# scraper.py (Updated to include event dates)

import random
from datetime import datetime, timedelta

# Mock function to simulate scraping NSE/BSE
def fetch_latest_announcements():
    companies = ["ADANIPORTS", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK"]
    random_triggers = ["CFO_EXIT", "AUDITOR_EXIT", "PLEDGE_SPIKE", "NCLT_ADMISSION", "STATUTORY_DEFAULT"]
    data = []
    for company in companies:
        n = random.randint(0, 2)
        events = []
        for _ in range(n):
            event_name = random.choice(random_triggers)
            event_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            events.append({"event": event_name, "date": event_date})
        data.append({"company": company, "events": events})
    return data
