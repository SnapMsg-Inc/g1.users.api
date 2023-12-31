from sqlmodel import (
    SQLModel, 
    Field,
    Column, 
    String, 
    JSON, 
    ARRAY, 
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
    email: str
    nick: str = Field(max_length=30) 
    fullname: str = Field(default=None, max_length=50)
    alias: str
    birthdate: date
#    interests_bk: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    interests: Optional[List[str]] = Field(default=[], sa_column=Column(ARRAY(String)))
    zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
    followers: int = 0
    follows: int = 0
    is_admin: bool = False
    is_blocked: bool = False
    ocupation: Optional[str] = Field(default=None, nullable=True, max_length=25)
    pic: str = ""
    
    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)
        d["birthdate"] = str(d["birthdate"])
        return d    

    class ConfigDict:
        arbitrary_types_allowed=True
    

class UserPublic(SQLModel):
    uid: str 
    alias: str
    nick: str
    followers: int = 0
    follows: int = 0
    interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
    pic: str
    is_admin: bool
    is_blocked: bool
    

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
    
    def model_dump(self):
        d = super().model_dump()
        d["birthdate"] = str(d["birthdate"])
        return d        
    
    class ConfigDict:
        from_attributes=True

    
class UserRead(SQLModel): 
    uid: Optional[str] = None
    email: Optional[EmailStr] = None
    nick: Optional[str] = None
    alias: Optional[str] = None


class UserUpdate(SQLModel): 
    nick: Optional[str] = None
    alias: Optional[str] = None
    zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
    interests: Optional[List[str]] = None
    ocupation: Optional[str] = None
    pic: Optional[str] = None
    is_admin: Optional[bool] = None
    is_blocked: Optional[bool] = None


class Follow(SQLModel, table=True): 
    __tablename__ = "follows"
    __table_args__ = (PrimaryKeyConstraint('uid', 'followed'),)
        
    uid: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
    followed: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
    
