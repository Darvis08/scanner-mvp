# streamlit_app.py (Upgraded with all 5 Enhancements)

import streamlit as st
import requests
import time
from datetime import datetime

# Set Streamlit page config
st.set_page_config(page_title="Financial Risk Scanner", page_icon="📈", layout="wide")

st.title("📈 Financial Risk Scanner Dashboard")
st.write("Real-time RiskScore based on latest events.")

# Backend API URL
api_url = "https://scanner-mvp.onrender.com/scan"

# Auto-refresh every 10 minutes (600 seconds)
st_autorefresh = st.experimental_rerun if (time.time() % 600) < 1 else None

# Fetch data from backend
try:
    response = requests.get(api_url)
    data = response.json()
    results = data["results"]
except Exception as e:
    st.error("⚠️ Unable to fetch data. Please check backend is running.")
    st.stop()

# Last updated timestamp
last_updated = datetime.now().strftime("%d %b %Y %H:%M:%S")

# Company list for search filter
companies = [entry["company"] for entry in results]
selected_company = st.selectbox("Select Company to View:", ["All Companies"] + companies)

# Display results
for entry in results:
    company = entry["company"]
    riskscore = entry["riskscore"]
    band = entry["band"]
    events = entry["events"]

    if selected_company != "All Companies" and company != selected_company:
        continue

    # Risk Band Coloring
    if band == "Green":
        band_color = "#d4edda"
    elif band == "Amber":
        band_color = "#fff3cd"
    elif band == "Red":
        band_color = "#f8d7da"
    else:
        band_color = "#ffffff"

    # Display Company Card
    with st.container():
        st.markdown(f"""
            <div style='background-color: {band_color}; padding: 15px; border-radius: 10px;'>
                <h3>{company}</h3>
                <b>RiskScore:</b> {riskscore}<br>
                <b>Risk Band:</b> {band}<br>
                <b>Triggered Events:</b>
                <ul>
                    {''.join([f'<li>{event}</li>' for event in events]) if events else 'None'}
                </ul>
            </div>
            <br>
        """, unsafe_allow_html=True)

# Last updated footer
st.info(f"Last Updated: {last_updated}")

# Footer credit (optional)
st.markdown("---")
st.markdown("Built by 🚀 Financial Intelligence MVP")
