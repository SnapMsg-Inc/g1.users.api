from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional


class UserInfo(BaseModel):  # for request serialization
	email: str
	fullname: str
	nick: str
	interests: List[str]
	zone: str

class User(BaseModel):  # for request serialization
	uid: str
	email: Optional[str]
	fullname: Optional[str]
	nick: str
	interests: List[str]
	followers: int
	followings: int
	zone: Optional[str]


async def create_user(user: UserInfo):
	return {"message": "User created"}


async def get_users() -> List[User]:
	return {"message": "Sample user"}


async def update_user(nick: str, interests: List[str]):
	return {"message": "User updated"}


async def delete_user(uid):
	return {"message": "User deleted"}


async def follow_user(uid, otheruid):
	return {"message": "Following added"}


async def unfollow_user(uid, otheruid):
	return {"message": "Following removed"}


async def get_recommended(uid) -> List[User]:
	return {"message": "Recommended users"}
