from sqlmodel import Field, SQLModel, Column, String, JSON, ARRAY
from typing import Set, List, Optional
from datetime import date


class User(SQLModel, table=True): 
	__tablename__ = "users"	
	
	uid: str = Field(default=None, primary_key=True)
	email: str
	fullname: str
	nick: str
	b_day: date
	interests: Optional[List[str]] = Field(default=[], sa_column=Column(JSON), nullable=True)
	#followers: Set[str] = Field(default=None , sa_column=Column(ARRAY(String())))
	#followings: Set[str] = Field(default=None , sa_column=Column(ARRAY(String())))
	zone: Optional[str] = Field(default=None, nullable=True)
	is_admin: bool = False


class UserCreate(SQLModel): 
	email: str
	fullname: str
	nick: str
	interests: Optional[List[str]]= Field(default=None, sa_column=Column(JSON))
	zone: Optional[str] = Field(default=None, nullable=True)
	b_day: date 


class UserRead(SQLModel): 
	uid: Optional[str] = None
	email: Optional[str] = None
	nick: Optional[str] = None


class UserUpdate(SQLModel): 
	nick: str
	zone: str
	interests: List[str] = Field(sa_column=Column(JSON))



class Follow(SQLModel, table=True):
	__tablename__ = "follows"

	# {uid} follows {followed_uid}
	fid: Optional[int] = Field(default=None, primary_key=True)
	uid: str
	followed_uid: str


