from pydantic import BaseModel


class User(BaseModel):
	uid: str
	nick: str
	fullname: str
	email: str


async def create_user():
	return {"message": "User created"}


async def get_user():
	return {"message": "Sample user"}

