import pytest
import requests
import re
import json

#should be run on the fresh db

timestamp_regex =r'\d{4}-\d{2}-\d{2}'
id_regex = r"^\d+"

@pytest.mark.parametrize("email,password,username",[("alex@gmail.com","easypassword","Alex"),
                                                    ("testing@gmail.com","1234567","Ivanov"),
                                                    ("moretest@gmail.com","SuPeRRPass","Petrov123")])
def test_register_new_users(email,password,username):
    pload = {"username": username, "password": password, "email": email}
    response = requests.post("http://127.0.0.1:8000/user/",json = pload)
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
def test_same_data(email, password, username):
    pload = {"username": username, "password": password, "email": email}
    response = requests.post("http://127.0.0.1:8000/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "User exist"}

#user data is too big
def test_long_data():
    pload = {"username": "Alex333333333333333333333333333333333333333333333333", "password": "password",
             "email": "alexmail3@gmail.com"}
    response = requests.post("http://127.0.0.1:8000/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "Bad data format"}

#user data is not acceptable, has ' ' in
def test_long_data():
    pload = {"username": "Alex 33", "password": "pass _word",
             "email": "alexmail3@gmail.com"}
    response = requests.post("http://127.0.0.1:8000/user/", json=pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json() == {"detail": "Bad data format"}