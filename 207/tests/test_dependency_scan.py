from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dependency_scan_admin():
    r = client.get("/security/dependency-scan", headers={"X-Role": "admin"})
    assert r.status_code in [200, 409]

def test_dependency_scan_denied():
    r = client.get("/security/dependency-scan", headers={"X-Role": "writer"})
    assert r.status_code == 403
