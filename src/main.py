from fastapi import FastAPI, Query, Depends
from typing import List, Optional, Annotated
from .models import User, UserCreate, UserRead, UserUpdate
from .database import init_tables
from . import crud


app = FastAPI()

@app.on_event("startup")
def on_startup():
	# connect to db and create tables 
    init_tables()


@app.get("/")
async def root():
	return {"message": "users microsevice"}


@app.post("/users/{uid}", status_code=201)
async def create_user(uid: str, user: UserCreate):
	crud.create_user(uid, user)
	return {"message": "user created"}


@app.get("/users", response_model=List[User])
async def get_users(user: UserRead = Depends(), limit: int = Query(default=100, le=100), page: int = 0):
	print(f"LIMIT {limit}")
	users = crud.read_users(user, limit, page)
	return users


@app.patch("/users/{uid}")
async def update_user(uid: str, user: UserUpdate):
	crud.update_user(uid, user)
	return {"message": "user updated"}


@app.delete("/users/{uid}")
async def delete_user(uid: str):
	crud.delete_user(uid)
	return {"message": "user deleted"}


@app.get("/users/{uid}/recommended")
async def get_recommended(uid: str) -> List[User]:
	return {"message": "recommended users"}


@app.get("/users/{uid}/followers", response_model=List[User])
def get_follows(uid: str, limit: int = Query(default=100, le=100), page: int = 0):
	return crud.read_followers(uid, limit, page)
	

@app.get("/users/{uid}/follows", response_model=List[User])
def get_follows(uid: str, limit: int = Query(default=100, le=100), page: int = 0):
	return crud.read_follows(uid, limit, page)
	

@app.post("/users/{uid}/follows/{otheruid}")
async def follow_user(uid: str, otheruid: str):
	crud.follow_user(uid, otheruid)
	return {"message": "follow added"}


@app.delete("/users/{uid}/follows/{otheruid}")
async def unfollow_user(uid, otheruid):
	crud.unfollow_user(uid, otheruid)
	return {"message": "follow removed"}




