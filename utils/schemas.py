from pydantic import BaseModel,EmailStr, constr
from typing import Optional
from datetime import datetime

class RegisterOut(BaseModel):
    id:Optional[int]
    username: str
    email: EmailStr
    register_date: Optional[datetime]

class RegisterIn(RegisterOut):
    password: str

class UserUpdate(RegisterOut):
    updated: Optional[str] = f"User updated at {datetime.now().date()}"

class UserList(BaseModel):
    username: str
    email: EmailStr

class UserListRaw(UserList):
    id: int
    register_date: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class PatchOut(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
class PatchIn(PatchOut):
    password: Optional[str]

class AccountRemoved(BaseModel):
    status: Optional[str] = "Account removed"
    id:Optional[int]
    username: str
    email: EmailStr
    register_date: Optional[datetime]
