import asyncpg.exceptions
from fastapi import APIRouter, HTTPException,status
from utils.database import database
from utils.schemas import PatchIn, PatchOut
from utils import models,pwd
from utils.pass_user import pass_user

router = APIRouter(tags=['patch_user'])

#Patch will return the data and 200 response code, even if we send same data that already exist under #id row
# Patch accepting 3 fields: username, email,password
# Can update up to 3 fields at the time, depending how many key-values we provide in the json request.

# send to endpoint: id in path(user you want to update), username + password + email (any of these 3, at least 1)
# response: account data(username/email) that has been updated


@router.patch("/user/{id}", response_model=PatchOut)
async def update_item(id: int, item: PatchIn):

    #check if account exist in the DB:
    account_query = models.users.select().where(id == models.users.c.id)
    account_check_result = await database.fetch_one(account_query)
    if not account_check_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")

    #check if there is password inside of an item
    updated_item=item.dict()
    for key,value in updated_item.items():
        if key != 'email' and value != None:
            if not pass_user(value):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong data format")
        #if password exist = hash it!
        if key == "password" and value != None:
            hashed_password = await pwd.hash(value)
            updated_item["password"]=hashed_password
    #data we get from the request
    goodmodel =  PatchIn(**updated_item)
    #stored_item_data_query = await database.fetch_one(models.users.select().where(models.users.c.id==id))
    stored_item_data = dict(account_check_result.items())
    # manipulate the data from db with pydantic models
    stored_item_model = PatchIn(**stored_item_data)

    # exclude the "none" fields and then merge the data into the final version, which will be "pushed" to the DB
    update_data = goodmodel.dict(exclude_none=True, exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    try:
        patch_query  = models.users.update().where(models.users.c.id == id).values(update_data)
        await database.execute(patch_query)
    except asyncpg.exceptions.PostgresSyntaxError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Please provide any of these: "
                                                                               "email,password,username "
                                                                               "key-value pairs data, other keys will be ignored")
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User with this data already exist")
    return updated_item

