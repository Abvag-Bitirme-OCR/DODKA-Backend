from fastapi.testclient import TestClient
from fastapi import status
import API
from API import main
client=TestClient(app=main.app)

def test_index_returns_correct():

    response=client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'Redis connection is successfuly!'
