from sqlmodel import Field, SQLModel, Column, String, JSON, ARRAY, ForeignKey, PrimaryKeyConstraint
from typing import Set, List, Optional


class User(SQLModel, table=True): 
	__tablename__ = "users"	

	uid: str = Field(default=None, primary_key=True)
	email: str
	fullname: str
	nick: str
	interests: List[str] = Field(default=[], sa_column=Column(JSON))
	zone: str
	is_admin: bool = False


class UserCreate(SQLModel): 
	email: str
	fullname: str
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))
	zone: str


class UserRead(SQLModel): 
	uid: Optional[str] = None
	email: Optional[str] = None
	nick: Optional[str] = None


class UserUpdate(SQLModel): 
	nick: str
	interests: List[str] = Field(default=None, sa_column=Column(JSON))



class Follow(SQLModel, table=True):
	class Follow(SQLModel, table=True):
		__tablename__ = "follows"
		__table_args__ = (
        PrimaryKeyConstraint("uid", "followed_uid"),
    )
	uid: str = Field(default=None, sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	followed_uid: str = Field(default=None, sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))

	# __tablename__ = "follows"

	# # {uid} follows {followed_uid}
	# fid: Optional[int] = Field(default=None, primary_key=True, auto_increment=True)
	# uid: str = Field(default=None, sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	# followed_uid: str = Field(default=None, sa_column=Column(String, ForeignKey('users.uid', ondelete='CASCADE')))
	# # fid: Optional[int] = Field(default=None, primary_key=True)
	# # uid: str
	# # followed_uid: str