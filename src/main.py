from fastapi import FastAPI, Query
from typing import List, Optional
from .models import User, UserCreate, UserUpdate
from .database import init_tables
from . import crud


app = FastAPI()

@app.on_event("startup")
def on_startup():
	# connect to db and create tables 
    init_tables()


@app.get("/")
async def root():
	return {"message": "Users microsevice"}


@app.post("/users/{uid}", status_code=201)
async def create_user(uid: str, user: UserCreate):
	crud.create_user(uid, user)
	return {"message": "User created"}


@app.get("/users", response_model=List[User])
async def get_users(uid: str = "", email: str = "", nick: str = "", page: int = 0, limit: int = Query(default=100, lte=100)):
	users = crud.read_users(limit, page, uid, email, nick)
	return users


@app.patch("/users/{uid}")
async def update_user(uid: str, user: UserUpdate):
	crud.update_user(uid, user)
	return {"message": "User updated"}


@app.delete("/users/{uid}")
async def delete_user(uid):
	return {"message": "User deleted"}


@app.post("/users/{uid}/follow/{otheruid}")
async def follow_user(uid, otheruid):
	return {"message": "Following added"}


@app.delete("/users/{uid}/follow/{otheruid}")
async def unfollow_user(uid, otheruid):
	return {"message": "Following removed"}


@app.get("/users/{uid}/recommended")
async def get_recommended(uid) -> List[User]:
	return {"message": "Recommended users"}




