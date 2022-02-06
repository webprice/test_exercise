import asyncpg.exceptions
from fastapi import APIRouter, HTTPException,status
from utils.database import database
from utils.schemas import RegisterOut ,UserLogin
from utils import models
from utils.account_check import account_check
router = APIRouter(tags=['get_user'])

#Get user by ID(provided in the path)
#requirements, in json: username + password of active account
#Returns whole data of the user, except password

@router.get("/user/{id}",response_model=RegisterOut, status_code=status.HTTP_200_OK)
async def user_get(id:int, user:UserLogin):

    # check if account has a permission to access the Data
    await account_check(user.username, user.password)

    # check the user by id from the path
    try:
        query = models.users.select().where(models.users.c.id==id)
        result = await database.fetch_one(query)
        #print(result)
        if result:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")
    except asyncpg.exceptions.DataError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)




