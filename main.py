from fastapi import FastAPI
#from sqlalchemy.testing import db

from utils.database import metadata,database
#from utils.database import engine
from routes import user_list,get_user,put_user_data,patch_user_data,delete,registration,ping

#App and database initialization
app = FastAPI()
#metadata.create_all(engine)

#This route is an extra
#we can specify statements before the db connection
#and the additional statements to run  after the connection close
#Here we establish the connection pool and close the connection pool

#Establish database connection each time any route called
@app.on_event("startup")
async def startup():
    await database.connect()

#Closing database connection each time any route called
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



#regular routes
app.include_router(user_list.router)
app.include_router(get_user.router)
app.include_router(put_user_data.router)
app.include_router(patch_user_data.router)
app.include_router(delete.router)
app.include_router(registration.router)
app.include_router(ping.router)


