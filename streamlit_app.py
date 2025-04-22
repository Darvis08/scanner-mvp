# streamlit_app.py
import streamlit as st
import requests

st.title("📈 Financial Risk Scanner Dashboard")

st.write("Real-time RiskScore based on latest events.")

# Fetch data from backend API
api_url = "https://scanner-mvp-production.up.railway.app/scan"  # (we will correct once deployed)
try:
    response = requests.get(api_url)
    data = response.json()
    results = data["results"]

    for company_data in results:
        st.subheader(f"{company_data['company']}")
        st.metric(label="RiskScore", value=company_data["riskscore"])
        st.write(f"Risk Band: {company_data['band']}")
        st.write("Triggered Events:", company_data["events"])
        st.divider()

except Exception as e:
    st.error("⚠️ Unable to fetch data. Please check backend is running.")

