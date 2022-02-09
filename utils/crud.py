from utils.models import users
from utils.database import database
from utils.schemas import RegisterIn
from pydantic import EmailStr

class Crud:
    async def read(id:int):
        query = users.select().where(users.c.id == id)
        return await database.fetch_one(query)

    async def read_by_email(email:EmailStr):
        query = users.select().where(users.c.email==email)
        return await database.fetch_one(query)

    async def read_all(id="not needed"):
        query = users.select()
        return await database.fetch_all(query)

    async def patch(id:int,update_data):
        patch_query = users.update().where(users.c.id == id).values(update_data)
        return await database.execute(patch_query)

    async def delete(id:int):
       remove_query = users.delete().where(users.c.id == id)
       return await database.execute(remove_query)
       #return result

    async def put(id:int,user:RegisterIn,hashed_password:str):
        query = users.update().where(users.c.id == id).values(email=user.email, password=hashed_password,
                                                                            username=user.username)
        return await database.execute(query)

    async def create(id: int, user: RegisterIn, hashed_password: str):
        query = users.insert().values(username=user.username, email=user.email, password=hashed_password)
        return await database.execute(query)