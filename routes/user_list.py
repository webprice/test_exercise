from typing import List
from fastapi import APIRouter
from utils.database import database
from utils.schemas import UserListRaw, UserList ,UserLogin
from utils import models
from utils.account_check import account_check
from utils.crud import Crud
router = APIRouter(tags=['user_list'])

#Get users lists

#required: username+password to access the endpoint's data
#I've hide passwords in both routers for the safety purposes
#get users list without passwords
@router.get("/user-list-raw/",response_model=List[UserListRaw])
async def user_get_list_raw(user: UserLogin):
    #check if account has a permission to access the Data
    await account_check(user.username,user.password)
    #get users list from the db
    # query = models.users.select()
    # return await database.fetch_all(query)
    return await Crud.read_all()

#get users list without passwords, IDs,register date
@router.get("/user-list/",response_model=List[UserList])
async def user_get_list(user: UserLogin):
    # check if account has a permission to access the Data
    await account_check(user.username, user.password)
    # get users list from the db
    #query = models.users.select()
    return await Crud.read_all()




