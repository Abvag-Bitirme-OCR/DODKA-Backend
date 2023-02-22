from fastapi.testclient import TestClient
from API import app

client = TestClient(app)

def test_read_main():
    response = client.get("/healthcheck")
    assert response.status_code == 500
    assert response.json() == {"message": "Hello World"}