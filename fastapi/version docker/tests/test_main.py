import pytest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bonjour"
    }

def read_item():
    response = client.get("/items/42?item_name=test")

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 42,
        "item_name": "test",
    }

def read_item_without_name():
    response = client.get("/items/42")

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 42,
        "name_item": None,
    }

@pytest.mark.parametrize(
    "item_id",
    ["abc", "1.1", "-1", "invalid"],
)
def read_item_with_invalid_id(item_id):
    response = client.get(f"/items/{item_id}")

    assert response.status_code == 422
    
def read_item_name_too_long():
    item_name = "a" * 101

    response = client.get(f"/items/42?item_name={item_name}")

    assert response.status_code == 422