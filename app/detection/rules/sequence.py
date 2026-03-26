def detect_sequence(event, context):
    user = event.get("user_id")

    recent_logins = context.get_recent_logins(user, 600)
    recent_tx = context.get_recent_transactions(user, 600)

    login_success = any(e[0] == "login_success" for e in recent_logins)

    if login_success and len(recent_tx) >= 1:
        return {
            "type": "SUSPICIOUS_SEQUENCE",
            "severity": "medium",
            "confidence": 75,
            "reason": "Login followed by transaction",
            "mitre": "T1078"
        }

    return None 
