import pytest
import requests
import json
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
#should be run after get_user test.
#send user data in json(user should have access to see the results)
#response should be list of accounts from the DB in JSON format

#user exist, gives back the correct answer, 200
@pytest.mark.parametrize("username,password",[("Alex","easypassword")])
def test_get_listofusers(client,username,password):
    pload = {"username": username, "password": password}
    response = client.get("/user-list",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200

#user did not exist , gives back the error, 404
@pytest.mark.parametrize("username,password",[("Alex_3","easypassword")])
def test_get_listofusers_wrong_data(client,username,password):
    pload = {"username": username, "password": password}
    response = client.get("/user-list",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json() == {"detail": "User doesn't exist"}


# /user-list-raw/ path testing:

#user exist, gives back the correct answer, 200
@pytest.mark.parametrize("username,password",[("Alex","easypassword")])
def test_get_listofusers_raw(client,username,password):
    pload = {"username": username, "password": password}
    response = client.get("/user-list-raw",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200

#user did not exist , gives back the error, 404
@pytest.mark.parametrize("username,password",[("Alex_3","easypassword")])
def test_get_listofusers_wrong_data_raw(client,username,password):
    pload = {"username": username, "password": password}
    response = client.get("/user-list-raw",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json() == {"detail": "User doesn't exist"}