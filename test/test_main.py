from fastapi.testclient import TestClient
from src.main import app  

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Users microsevice"}

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "get users"}
