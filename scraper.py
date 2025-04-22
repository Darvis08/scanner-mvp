# scraper.py
import random

# Mock function to simulate scraping NSE/BSE
def fetch_latest_announcements():
    companies = ["ADANIPORTS", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK"]
    random_triggers = ["CFO_EXIT", "AUDITOR_EXIT", "PLEDGE_SPIKE", "NCLT_ADMISSION", "STATUTORY_DEFAULT"]
    data = []
    for company in companies:
        triggers = random.sample(random_triggers, random.randint(0, 2))
        data.append({"company": company, "events": triggers})
    return data
