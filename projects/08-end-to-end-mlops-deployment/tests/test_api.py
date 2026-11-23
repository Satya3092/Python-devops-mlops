"""API tests (conftest.py trains a model first)."""
from fastapi.testclient import TestClient

from app import app

GOOD = {"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}
CALM = {"cpu_usage": 20, "memory_usage": 30, "disk_usage": 40, "error_count": 0, "response_time_ms": 120}


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["model_loaded"] is True


def test_predict_risky_server():
    with TestClient(app) as client:
        body = client.post("/predict", json=GOOD).json()
        assert body["failure"] is True
        assert 0.0 <= body["probability"] <= 1.0


def test_predict_calm_server():
    with TestClient(app) as client:
        assert client.post("/predict", json=CALM).json()["failure"] is False


def test_validation_error():
    with TestClient(app) as client:
        response = client.post("/predict", json={**GOOD, "cpu_usage": 150})
        assert response.status_code == 422


def test_batch():
    with TestClient(app) as client:
        response = client.post("/predict/batch", json=[GOOD, CALM])
        assert [p["failure"] for p in response.json()] == [True, False]



def test_metrics_endpoint_counts_predictions():
    with TestClient(app) as client:
        client.post("/predict", json=GOOD)
        text = client.get("/metrics").text
        assert 'predictions_total{outcome="failure"}' in text
        assert "http_requests_total" in text
