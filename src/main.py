from fastapi import FastAPI, HTTPException, Header, Query, Depends
from sqlmodel import Session
from typing import List, Optional, Annotated
from .models import User, UserPublic, UserCreate, UserRead, UserUpdate
from .database import engine, init_tables
from . import crud

import datadog 
from ddtrace.runtime import RuntimeMetrics

RuntimeMetrics.enable()

app = FastAPI()


def get_db():
    with Session(engine) as db:
        yield db

@app.on_event("startup")
def on_startup():
    # connect to db and create tables
    init_tables()


@app.get("/")
async def root():
    return {"message": "users microsevice"}


@app.post("/users/{uid}", status_code=201)
async def create_user(*,
                      db: Session = Depends(get_db),
                      uid: str,
                      user: UserCreate):
    crud.create_user(db, uid, user)
    return {"message": "user created"}


@app.get("/users", response_model=List[UserPublic])
async def get_users(*,
                    db: Session = Depends(get_db),
                    user: UserRead = Depends(),
                    limit: int = Query(default=100, le=100),
                    page: int = 0):
    print(f"LIMIT {limit}")
    users = crud.read_users(db, user, limit, page)
    return users


@app.get("/users/{uid}", response_model=User)
def get_user(*, db: Session = Depends(get_db), uid: str):
	return crud.read_user(db, uid)


@app.patch("/users/{uid}")
async def update_user(*,
                      db: Session = Depends(get_db),
                      uid: str,
                      user: UserUpdate):
    crud.update_user(db, uid, user)
    return {"message": "user updated"}


@app.delete("/users/{uid}")
async def delete_user(*, db: Session = Depends(get_db), uid: str):
    crud.delete_user(db, uid)
    return {"message": "user deleted"}


@app.get("/users/{uid}/recommended", response_model=List[UserPublic])
async def get_recommended(*, db: Session = Depends(get_db), uid: str):
    return {"message": "recommended users"}


@app.get("/users/{uid}/followers", response_model=List[UserPublic])
def get_followers(*,
                  db: Session = Depends(get_db),
                  uid: str,
                  limit: int = Query(default=100, le=100),
                  page: int = 0):
    return crud.read_followers(db, uid, limit, page)


@app.get("/users/{uid}/follows", response_model=List[UserPublic])
def get_follows(*,
                db: Session = Depends(get_db),
                uid: str,
                limit: int = Query(default=100, le=100),
                page: int = 0):
    return crud.read_follows(db, uid, limit, page)


@app.get("/users/{uid}/follows/{otheruid}")
async def get_follow(*, db: Session = Depends(get_db), uid: str, otheruid: str):
    if not crud.read_follow(db, uid, otheruid):
        raise HTTPException(status_code=404, detail="follow not found")
    return {"message": "follow exists"}


@app.post("/users/{uid}/follows/{otheruid}")
async def follow_user(*, db: Session = Depends(get_db), uid: str,
                      otheruid: str):
    crud.follow_user(db, uid, otheruid)
    return {"message": "follow added"}


@app.delete("/users/{uid}/follows/{otheruid}")
async def unfollow_user(*, db: Session = Depends(get_db), uid, otheruid):
    crud.unfollow_user(db, uid, otheruid)
    return {"message": "follow removed"}

