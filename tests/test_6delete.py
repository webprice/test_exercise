import pytest
import requests
import re
import json


#user should be logged in to remove another users
#user will be removed by {id} number
#user removing itself
@pytest.mark.parametrize("id,password,username",[("2","1234567","Ivanov")])
def test_delete_user(id,password,username):
    pload = {"username": username, "password": password}
    response = requests.delete(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200

#user removing another user
@pytest.mark.parametrize("id,password,username",[("3","easypassword","Alex"),])
def test_delete_user_another(id,password,username):
    pload = {"username": username, "password": password}
    response = requests.delete(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200

#user doesn't exist in the db, error 404
@pytest.mark.parametrize("id,password,username",[("333","easypassword","Alex"),])
def test_delete_user_id_404(id,password,username):
    pload = {"username": username, "password": password}
    response = requests.delete(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json() == {"detail": "Account doesn't exist"}


#wrong data in JSON
@pytest.mark.parametrize("id,password,username",[("1","easypa ssword","Alex"),
                                                 ("1","easypassword","_ Alex"),])
def test_delete_wrong_json(id,password,username):
    pload = {"username": username, "password": password}
    response = requests.delete(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    #assert response.json() == {"detail": "Account doesn't exist"}


#removing the 1st user, finish.
@pytest.mark.parametrize("id,password,username",[("1","easypassword","Alex")])
def test_delete_1stuser(id,password,username):
    pload = {"username": username, "password": password}
    response = requests.delete(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200