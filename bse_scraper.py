# bse_scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

def fetch_bse_announcements():
    url = "https://www.bseindia.com/corporates/ann.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    announcements = []

    table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvData"})
    if table:
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows[:100]:  # Only latest 100 entries
            cols = row.find_all("td")
            if len(cols) >= 5:
                company = cols[0].text.strip()
                subject = cols[3].text.strip()
                announce_datetime = cols[4].text.strip()

                try:
                    announce_date = datetime.strptime(announce_datetime.split()[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    announce_date = None

                announcements.append({
                    "company": company,
                    "subject": subject,
                    "date": announce_date
                })

                time.sleep(random.uniform(0.5, 1.0))

    return announcements

# For local testing
if __name__ == "__main__":
    data = fetch_bse_announcements()
    for entry in data:
        print(entry)
