from fastapi import HTTPException,status
from utils.database import database
from utils import models,pwd


#Function checking if user registered
#wrong password or not(in the DB)
async def account_check(get_username,get_password):
    account_query = models.users.select().where(get_username == models.users.c.username)
    account_check_result = await database.fetch_one(account_query)
    if not account_check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
    if not await pwd.verify(get_password,account_check_result["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong password")
    return True
