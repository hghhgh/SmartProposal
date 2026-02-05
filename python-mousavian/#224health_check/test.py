import requests

HEALTH_URL = "http://localhost:8000/health"

def test_health_endpoint():
    response = requests.get(HEALTH_URL, timeout=3)

    assert response.status_code == 200, "❌ Health endpoint not responding"
    assert response.json().get("status") == "ok", "❌ Health status is not ok"

    print("✅ Health check passed successfully")


if __name__ == "__main__":
    test_health_endpoint()
