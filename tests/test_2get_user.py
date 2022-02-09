import pytest
import json
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
#should be run after test_registration test.
#user exist under db
@pytest.mark.parametrize("id,username,password",[("1","Alex","easypassword")])
def test_get_existing_user(client,id,username,password):
    pload = {"username": username, "password": password}
    response = client.get(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200


#user did not exist 404, wrong id
@pytest.mark.parametrize("id,username,password",[("999","Alex","easypassword")])
def test_get_user_dnt_exist(client,id,username,password):
    pload = {"username": username, "password": password}
    response = client.get(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json() == {'detail': "Account doesn't exist"}

#Wrong data in Json
@pytest.mark.parametrize("id,username,password",[("1","Alex_3","easypassword"),])
def test_get_user_data_not_acceptable(client,id,username,password):
    pload = {"username": username, "password": password}
    response = client.get(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json() == {'detail': "User doesn't exist"}