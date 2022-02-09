import pytest
import re
import json
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

#should be run on the fresh db

timestamp_regex =r'\d{4}-\d{2}-\d{2}'
id_regex = r"^\d+"

@pytest.mark.parametrize("email,password,username",[("alex@gmail.com","easypassword","Alex"),
                                                    ("testing@gmail.com","1234567","Ivanov"),
                                                    ("moretest@gmail.com","SuPeRRPass","Petrov123")])
def test_register_new_users(client,email,password,username):
    pload = {"username": username, "password": password, "email": email}
    response = client.post("/user/",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    reg_date = response.json()["register_date"]
    id = response.json()["id"]
    assert bool(re.match(id_regex, str(id))) == True
    assert response.json()["email"] == email
    assert response.json()["username"] == username
    assert bool(re.match(timestamp_regex, str(reg_date))) == True
    assert response.status_code == 200


#user exist
@pytest.mark.parametrize("email,password,username",[("alex@gmail.com","easypassword","Alex"),
                                                    ("testing@gmail.com","1234567","Ivanov"),
                                                    ("moretest@gmail.com","SuPeRRPass","Petrov123")])
def test_same_data(client,email, password, username):
    pload = {"username": username, "password": password, "email": email}
    response = client.post("/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "User exist"}

#user data is too big
def test_long_data(client):
    pload = {"username": "Alex333333333333333333333333333333333333333333333333", "password": "password",
             "email": "alexmail3@gmail.com"}
    response = client.post("/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "Bad data format"}

#user data is not acceptable, has ' ' in
def test_long_data(client):
    pload = {"username": "Alex 33", "password": "pass _word",
             "email": "alexmail3@gmail.com"}
    response = client.post("/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "Bad data format"}