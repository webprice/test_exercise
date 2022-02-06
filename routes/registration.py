import asyncpg.exceptions
from fastapi import APIRouter, HTTPException,status
from utils.database import database
from utils.schemas import RegisterOut,RegisterIn
from utils import models,pwd
from utils.pass_user import pass_user
router = APIRouter(tags=['registration'])

#user registration route
#Required: username, email, password key-values pairs
#returns: id, username, email, register_date. exclude password.
@router.post("/user/", response_model=RegisterOut,status_code=200)
async def user_post(user: RegisterIn):
    try:
        #check pass login
        if not pass_user(user.username,user.password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail="Bad data format")

        # hash the password user.pasword
        hashed_password = await pwd.hash(user.password)
        query = models.users.insert().values(username=user.username, email=user.email,password=hashed_password)
        result = await database.execute(query)

    #this exception will work only if someone registered with email/username that is already taken in the DB
    #The ID of the user will have gaps between numbers(previous users) if spam same data over and over again
    #The official explanation next:
    #Important: To avoid blocking concurrent transactions that obtain numbers from the same sequence, a nextval
    # operation is never rolled back; that is, once a value has been fetched it is considered used and will not be
    # returned again. This is true even if the surrounding transaction later aborts, or if the calling query ends up
    # not using the value.
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail="User exist")

    #if user gives a way too long data
    except asyncpg.exceptions.StringDataRightTruncationError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The data is too big")

    #check the newly created user and return it's data
    check_query = models.users.select().where(models.users.c.email==user.email)
    #timestamp can be overwritten in pretty manner:
    #user.register_date = str(query["register_date"].date())
    return await database.fetch_one(check_query)
