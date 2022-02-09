from fastapi.testclient import TestClient

from main import app
import json

client = TestClient(app)

def test_ping(client):
    payload ={"username":"Alex","password":"easypassword"}
    response = client.get("/user/3", json=payload)
    print(response.status_code,"")
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200
    assert response.json() == {
    "email": "alex@gmail.com",
    "id": 3,
    "register_date": "2022-02-08T14:36:47.620395+00:00",
    "username": "Alex"
}
