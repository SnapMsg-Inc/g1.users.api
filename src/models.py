from sqlmodel import Field, SQLModel, Column, String, JSON, ARRAY, ForeignKey, PrimaryKeyConstraint
from typing import Set, List, Optional, Pattern, Annotated
from datetime import datetime, date, timedelta
from pydantic import validator, BaseModel



class User(SQLModel, table=True): 
	__tablename__ = "users"	
	
	uid: str = Field(default=None, primary_key=True)
	email: str
	fullname: str = Field(default=None, max_length=50)
	nick: str
	birthdate: date
	interests: Optional[List[str]] = Field(default=[], sa_column=Column(JSON), nullable=True)
	zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
	followers: int = 0
	follows: int = 0
	is_admin: bool = False
	ocupation: Optional[str] = Field(default=None, nullable=True, max_length=25)
	pic: Optional[str] = "" 
	
	class Config:
		arbitrary_types_allowed=True
	

class UserPublic(SQLModel):
	uid: str 
	nick: str
	followers: int = 0
	follows: int = 0
	interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
	pic: Optional[str]
	

class UserCreate(SQLModel): 
	email: str = Field(regex=r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
	fullname: str
	nick: str
	interests: Optional[List[str]] = []
	zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
	birthdate: date
	ocupation: Optional[str] = None
	pic: Optional[str] = None


class UserRead(SQLModel): 
	uid: Optional[str] = None
	email: Optional[str] = None
	nick: Optional[str] = None


class UserUpdate(SQLModel): 
	nick: Optional[str]
	zone: Optional[dict[str, float]] = Field(default={}, sa_column=Column(JSON))
	interests: Optional[List[str]]
	ocupation: Optional[str]
	pic: Optional[str]


class Follow(SQLModel, table=True):	
	__tablename__ = "follows"
	__table_args__ = (PrimaryKeyConstraint('uid', 'followed'),)
		
	uid: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	followed: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	
