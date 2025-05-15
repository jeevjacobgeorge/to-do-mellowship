from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserIn(User):
    password:str

class UserInDB(User,table=True):
    username:str = Field(primary_key=True)
    hashed_password: str
    todos:list["Todo"] = Relationship(back_populates="owner")
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime

class Todo(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    title:str
    description:Optional[str] = None
    deadline:datetime | None = None
    completed:bool = False
    owner_username: str = Field(foreign_key="userindb.username")
    owner: Optional["UserInDB"] = Relationship(back_populates="todos")
    class Config:
        orm_mode = True
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None

