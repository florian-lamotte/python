from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bonjour"
    }

def test_read_item():
    response = client.get("/items/42?q=test")

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 42,
        "q": "test",
    }

def test_invalid_item_id():
    response = client.get("/items/abc")

    assert response.status_code == 422