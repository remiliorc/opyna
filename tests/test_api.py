from fastapi.testclient import TestClient

from opyna.api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze():
    r = client.post("/analyze", json={"review": "buena batería", "aspects": ["batería"]})
    assert r.status_code == 200
    assert r.json()["results"][0]["aspect"] == "batería"
