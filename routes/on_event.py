from fastapi import APIRouter
from utils.database import database as db

router = APIRouter(tags=['on_event'])

#Establish database connection each time any route called
@router.on_event("startup")
async def startup():
    await db.connect()

#Closing database connection each time any route called
@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()