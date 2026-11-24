from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mini Order Service is running!"}

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200

def test_invalid_order_request():
    response = client.post("/orders", json={})
    assert response.status_code == 422
