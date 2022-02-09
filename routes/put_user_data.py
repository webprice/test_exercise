import asyncpg.exceptions
from fastapi import APIRouter, HTTPException,status
from utils.database import database
from utils.schemas import RegisterIn,UserUpdate
from utils import models,pwd
from utils.pass_user import pass_user
from utils.crud import Crud
router = APIRouter(tags=['put_user_data'])

#PUT will overwrite the whole data of the user
#required in json: username, email, password, id in path
#RETURNS: whole data of the updated user(except password)

@router.put("/user/{id}", response_model=UserUpdate)
async def user_put(id:int, user:RegisterIn):

    # check pass login format
    if not pass_user(user.username, user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Bad data format")

    #check if user with ID exist:
    #checkquery = models.users.select().where(models.users.c.id==id)
    if not await Crud.read(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this id:{id} does not exist")

    #send the updated data to replace the old data in the db
    try:
        hashed_password = await pwd.hash(user.password)
        #query = models.users.update().where(models.users.c.id==id).values(email=user.email, password=hashed_password, username=user.username)
        #await database.execute(query)
        await Crud.put(id,user,hashed_password)

        #get the new data of the user
        # checkq = models.users.select().where(models.users.c.id==id)
        # check_query = await database.fetch_one(checkq)

    except asyncpg.exceptions.DataError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong data format")
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User with this data already exist")

    return await Crud.read(id)
