from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ids_logs_403():
    client.get("/dashboard", headers={"X-Role": "writer"})
    r = client.get("/dashboard", headers={"X-Role": "admin"})
    assert r.status_code == 200
