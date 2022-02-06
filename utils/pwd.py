from passlib.context import CryptContext
from fastapi import HTTPException,status
pwd_contex = CryptContext(schemes=['bcrypt'], deprecated="auto")

async def hash(password: str):
    return pwd_contex.hash(password)

async def verify(plain_password, hashed_password):
    try:
        #x = pwd_contex.verify(plain_password,hashed_password)

        return pwd_contex.verify(plain_password,hashed_password)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="wrong credentials")
