import pytest
import requests
import json
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
#PUT Required all 3 fields(email,username,password), if success it will replace all this data in the db
#send user data in json(user should have access to see the results)
#user with id exist in the database, gives back the correct answer, 200

@pytest.mark.parametrize("id,username,email,password",[("1","Alex","alex@gmail.com","easypassword")])
def test_put_user(client,id,username,email,password):
    pload = {"username": username,"email":email, "password": password}
    response = client.put(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 200


#user with id DID NOT exist in the database, gives back the answer 200
@pytest.mark.parametrize("id,username,email,password",[("333","Alex","alex@gmail.com","easypassword")])
def test_put_usernot_exist_in_db(client,id,username,email,password):
    pload = {"username": username,"email":email, "password": password}
    response = client.put(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 404
    assert response.json()== {"detail": f"User with this id:{id} does not exist"}


#user with id exist in the database, but data(username or pass) in json is corrupted, gives back the answer 406
@pytest.mark.parametrize("id,username,email,password",[("1","Alex _3","alex@gmail.com","easypassword"),
                                                       ("1","Alex","alex@gmail.com","easy password")])
def test_put_user_wrong_data(client,id,username,email,password):
    pload = {"username": username,"email":email, "password": password}
    response = client.put(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json()== {"detail": 'Bad data format'}

#user did not provided required fields for json request(one of these: email, username or password)
#other field wil lbe ignored
def test_patch_user_miss_data(client):
    pload = {"nickname": "Alex"}
    id=1
    response = client.patch(f"/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json()== {"detail": "Please provide any of these: email,password,username key-value pairs data, other keys will be ignored"}



#user with this details already exists. We send JSON with data that exist in DB, but it's associated with another user
@pytest.mark.parametrize("id,username,email,password",[("2","Alex","alex@gmail.com","easypassword"),])
def test_put_user_same_data(id,username,email,password):
    pload = {"username": username,"email":email, "password": password}
    response = requests.put(f"http://127.0.0.1:8000/user/{id}",json = pload)
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    assert response.status_code == 406
    assert response.json()== {"detail": "User with this data already exist"}
