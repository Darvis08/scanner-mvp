# event_detector.py

risk_keywords = {
    "CFO_EXIT": ["resignation of cfo", "change of cfo", "cfo resigned"],
    "AUDITOR_EXIT": ["auditor resigned", "resignation of auditor", "auditor resignation"],
    "STATUTORY_DEFAULT": ["default", "statutory default", "failure to repay", "payment default"],
    "NCLT_ADMISSION": ["nclt", "insolvency", "ibc admission", "corporate insolvency resolution"]
}

def detect_risk_event(subject):
    subject_lower = subject.lower()

    for event_type, keywords in risk_keywords.items():
        for keyword in keywords:
            if keyword in subject_lower:
                return event_type

    return None  # No Risk Event Detected
