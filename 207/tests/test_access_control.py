from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_admin_allowed():
    r = client.get("/dashboard", headers={"X-Role": "admin"})
    assert r.status_code == 200

def test_dashboard_denied():
    r = client.get("/dashboard", headers={"X-Role": "writer"})
    assert r.status_code == 403
