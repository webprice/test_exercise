import asyncpg.exceptions
from fastapi import APIRouter, HTTPException,status
from utils.database import database
from utils.schemas import UserLogin,AccountRemoved
from utils import models
from utils.account_check import account_check
router = APIRouter(tags=['delete'])

# required the active account to perform delete actions
# send to endpoint: id in path, username + password
# response: account data that has been removed


@router.delete("/user/{id}",response_model=AccountRemoved,status_code=status.HTTP_200_OK)
async def user_get(id:int, user:UserLogin):
    # check if account has a permission to access the Data
    await account_check(user.username, user.password)
    try:
        #check if account we want to delete exist:
        query = models.users.select().where(models.users.c.id==id)
        result = await database.fetch_one(query)
        #print(result)

        #if account that we want to delete exists in the db, deleting it:
        if result:
            remove_query= models.users.delete().where(models.users.c.id==id)
            #print(remove_query)
            await database.execute(remove_query)
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")
    except asyncpg.exceptions.DataError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)