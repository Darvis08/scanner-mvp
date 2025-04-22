# risk_engine.py (Fixed)

rules = {
    "CFO_EXIT": 10,
    "AUDITOR_EXIT": 10,
    "PLEDGE_SPIKE": 8,
    "NCLT_ADMISSION": 10,
    "STATUTORY_DEFAULT": 9
}

def calculate_riskscore(events):
    score = sum(rules.get(event["event"], 0) for event in events)
    if score >= 80:
        band = "Severe Red"
    elif score >= 70:
        band = "Red"
    elif score >= 40:
        band = "Amber"
    else:
        band = "Green"
    return score, band
