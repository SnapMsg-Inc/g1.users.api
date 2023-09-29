from sqlmodel import Field, SQLModel, Column, String, JSON, ARRAY, ForeignKey, PrimaryKeyConstraint
from typing import Set, List, Optional
from datetime import date


class User(SQLModel, table=True): 
	__tablename__ = "users"	
	
	uid: str = Field(default=None, primary_key=True)
	email: str
	fullname: str
	nick: str
	birthdate: date
	interests: Optional[List[str]] = Field(default=[], sa_column=Column(JSON), nullable=True)
	zone: Optional[str] = Field(default=None, nullable=True)
	is_admin: bool = False
	description: Optional[str] = Field(default=None, nullable=True)
	ocupation: Optional[str] = Field(default=None, nullable=True)
	pic: Optional[str] = "" 
	

class UserPublic(SQLModel):
	uid: str 
	nick: str
	interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
	pic: Optional[str]
	

class UserCreate(SQLModel): 
	email: str
	fullname: str
	nick: str
	interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
	zone: Optional[str] = Field(default=None, nullable=True)
	birthdate: date
	description: Optional[str] = Field(default=None, nullable=True)
	ocupation: Optional[str] = Field(default=None, nullable=True) 
	pic: Optional[str]


class UserRead(SQLModel): 
	uid: Optional[str] = None
	email: Optional[str] = None
	nick: Optional[str] = None


class UserUpdate(SQLModel): 
	nick: Optional[str]
	zone: Optional[str]
	interests: List[str] = Field(sa_column=Column(JSON))
	description: Optional[str]
	ocupation: Optional[str]
	pic: Optional[str]


class Follow(SQLModel, table=True):	
	__tablename__ = "follows"
	__table_args__ = (PrimaryKeyConstraint('uid', 'followed'),)
		
	uid: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	followed: str = Field(sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	
