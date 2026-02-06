import requests
from app.core.security_events import log_event

def test_service_encryption(target_url: str, cert_path: str):
    try:
        response = requests.get(target_url, verify=cert_path)
        if response.status_code == 200:
            log_event("INTERNAL_COMM_SECURE", {"url": target_url, "status": "TLS verified"})
            return {"status": "secure", "url": target_url}
        else:
            log_event("INTERNAL_COMM_ERROR", {"url": target_url, "status": response.status_code})
            return {"status": "error", "url": target_url, "code": response.status_code}
    except requests.exceptions.SSLError as e:
        log_event("INTERNAL_COMM_TLS_ERROR", {"url": target_url, "error": str(e)})
        return {"status": "tls_error", "url": target_url, "error": str(e)}
