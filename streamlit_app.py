# streamlit_app.py (Professional Bloomberg-like UI)

import streamlit as st
import requests
import time
from datetime import datetime

# Set Streamlit page config
st.set_page_config(page_title="Financial Risk Scanner", page_icon="📈", layout="wide")

# Backend API URL
api_url = "https://scanner-mvp.onrender.com/scan"  # Correct your API URL here

# Auto-refresh every 10 minutes (600 sec)
st_autorefresh = st.experimental_rerun if (time.time() % 600) < 1 else None

# Header
st.title("📈 Financial Risk Scanner Dashboard")
st.markdown("""
Real-time RiskScore and Event Timeline for Listed Companies.
""")

# Fetch data
try:
    response = requests.get(api_url)
    data = response.json()
    results = data["results"]
except Exception as e:
    st.error("⚠️ Unable to fetch data. Please check backend is running.")
    st.stop()

# Last updated timestamp
last_updated = datetime.now().strftime("%d %b %Y %H:%M:%S")

# Company filter
companies = [entry["company"] for entry in results]
selected_company = st.selectbox("Select Company to View:", ["All Companies"] + companies)

# Display companies
for entry in results:
    company = entry["company"]
    riskscore = entry["riskscore"]
    band = entry["band"]
    events = entry["events"]

    if selected_company != "All Companies" and company != selected_company:
        continue

    # Risk Band Color
    if band == "Green":
        card_color = "#e6f4ea"
    elif band == "Amber":
        card_color = "#fff8e5"
    elif band == "Red":
        card_color = "#fdecea"
    else:
        card_color = "#ffffff"

    # Render company card
    with st.container():
        st.markdown(f"""
        <div style='background-color: {card_color}; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px #ddd;'>
            <h2 style='margin-bottom: 0;'>{company} <span style='font-size:16px; color:gray;'>[{band}]</span></h2>
            <h4 style='margin-top: 5px;'>RiskScore: <span style='color:black;'>{riskscore}</span></h4>
            <hr>
            <h5>Triggered Events:</h5>
            <ul>
        """, unsafe_allow_html=True)

        if events:
            for event in events:
                st.markdown(f"<li>{event['date']} ➔ {event['event']}</li>", unsafe_allow_html=True)
        else:
            st.markdown("<li>No Events</li>", unsafe_allow_html=True)

        st.markdown("""
            </ul>
        </div>
        <br>
        """, unsafe_allow_html=True)

# Last updated timestamp
st.info(f"Last Updated: {last_updated}")

# Footer credit
st.markdown("""
---
Built by 🚀 Financial Intelligence MVP | Powered by Streamlit Cloud
""")
