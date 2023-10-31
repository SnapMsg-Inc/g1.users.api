from sqlmodel import (
    SQLModel, 
    Field,
    Column, 
    String, 
    JSON, 
    ForeignKey, 
    UniqueConstraint,
    PrimaryKeyConstraint
)
from typing import Set, List, Optional, Pattern, Annotated
from datetime import datetime, date, timedelta
from pydantic import BaseModel, EmailStr, HttpUrl, validator



class User(SQLModel, table=True): 
    __tablename__ = "users" 
    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("nick"),
    )
    
    uid: str = Field(default=None, primary_key=True)
    email: EmailStr
    nick: str = Field(max_length=30) 
    fullname: str = Field(default=None, max_length=50)
    alias: str
    birthdate: date
    interests: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
    followers: int = 0
    follows: int = 0
    is_admin: bool = False
    ocupation: Optional[str] = Field(default=None, nullable=True, max_length=25)
    pic: str = ""
    
    class Config:
        arbitrary_types_allowed=True
    

class UserPublic(SQLModel):
    uid: str 
    alias: str
    nick: str
    followers: int = 0
    follows: int = 0
    interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
    pic: str
    

class UserCreate(SQLModel): 
    email: EmailStr 
    fullname: str
    alias: str
    nick: str
    interests: Optional[List[str]] = []
    zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
    birthdate: date
    ocupation: Optional[str] = None
    pic: str

    
class UserRead(SQLModel): 
    uid: Optional[str] = None
    email: Optional[EmailStr] = None
    nick: Optional[str] = None
    alias: Optional[str] = None


class UserUpdate(SQLModel): 
    alias: Optional[str]
    nick: Optional[str]
    zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
    interests: Optional[List[str]]
    ocupation: Optional[str]
    pic: str


class Follow(SQLModel, table=True): 
    __tablename__ = "follows"
    __table_args__ = (PrimaryKeyConstraint('uid', 'followed'),)
        
    uid: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
    followed: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
    
