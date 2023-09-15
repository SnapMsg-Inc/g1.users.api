from sqlmodel import Field, SQLModel, Column, JSON
from typing import List, Optional


class User(SQLModel, table=True): 
	__tablename__ = "users"	

	uid: str = Field(default=None, primary_key=True)
	email: str
	fullname: str
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))
	followers: int = 0
	followings: int = 0
	zone: str
	is_admin: bool = False


class UserCreate(SQLModel): 
	email: str
	fullname: str
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))
	zone: str


class UserRead(SQLModel): 
	uid: str
	email: Optional[str] = ""
	fullname: Optional[str] = ""
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))
	followers: int
	followings: int
	zone: Optional[str] = ""
	is_admin: bool


class UserUpdate(SQLModel): 
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))


