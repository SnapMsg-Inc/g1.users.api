from fastapi import FastAPI, HTTPException, Header, Query, Depends, Request
from fastapi.responses import JSONResponse 
from sqlmodel import Session
from contextlib import asynccontextmanager
from typing import List, Optional, Annotated
from pydantic import ValidationError
from .models import User, UserPublic, UserCreate, UserRead, UserUpdate
from .database import engine, init_tables
from . import crud

from datadog import initialize, DogStatsd
from ddtrace.runtime import RuntimeMetrics
from ddtrace import tracer

RuntimeMetrics.enable()

app = FastAPI()


options = {
    'statsd_host': 'datadog-agent',
    'statsd_port': 8125,
}
initialize(**options)
statsd = DogStatsd()


@app.exception_handler(Exception)
async def error_handler(req: Request, exc):
    detail = "internal server error"
    code = 400
    if isinstance(exc, ValidationError):
        detail = str(exc)
        code = 422 
    if isinstance(exc, crud.CRUDException):
        detail = str(exc)
        code = exc.code
    return JSONResponse(status_code=code, content={"detail" : detail})
 
def get_db():
    with Session(engine) as db:
        yield db

@asynccontextmanager
def on_startup():
    # connect to db and create tables
    init_tables()
    yield


@app.get("/")
def root():
    return {"message": "users microsevice"}


@app.post("/users/{uid}", status_code=201)
def create_user(*,
                db: Session = Depends(get_db),
                uid: str,
                user: UserCreate):
    crud.create_user(db, uid, user)

    if "latitude" in user.zone and "longitude" in user.zone:
        geo_tags = [f'latitude:{user.zone["latitude"]}', f'longitude:{user.zone["longitude"]}'] 
        print(f'[INFO] {geo_tags}')
        statsd.increment(metric="users.geo", tags=geo_tags.append("env:prod"))
    return {"message": "user created"}


@app.get("/users", response_model=List[UserPublic])
def get_users(*,
              db: Session = Depends(get_db),
              user: UserRead = Depends(),
              limit: int = Query(default=100, le=100),
              page: int = 0):
    users = crud.read_users(db, user, limit, page)
    return users


@app.get("/users/{uid}", response_model=User)
def get_user(*, db: Session = Depends(get_db), uid: str):
    user = crud.read_user(db, uid)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.patch("/users/{uid}")
def update_user(*,
                db: Session = Depends(get_db),
                uid: str,
                user: Optional[UserUpdate] = None):
    if not user:
        return {"message" : "nothing to update"}

    # check if user had valid geo info and decrement it
    db_user = crud.read_user(db, uid)
    old_zone = {}

    if db_user:
        old_zone = db_user.zone

    if "latitude" in old_zone and "longitude" in old_zone:
        geo_tags = [f'latitude:{old_zone["latitude"]}', f'longitude:{old_zone["longitude"]}'] 
        statsd.decrement(metric="users.geo", tags=geo_tags.append("env:prod"))
    
    crud.update_user(db, uid, user)

    # if success, increment geo data metric
    if "latitude" in user.zone and "longitude" in user.zone:
        geo_tags = [f'latitude:{user.zone["latitude"]}', f'longitude:{user.zone["longitude"]}'] 
        statsd.increment(metric="users.geo", tags=geo_tags.append("env:prod"))
    
    return {"message": "user updated"}

@app.delete("/users/{uid}")
def delete_user(*, db: Session = Depends(get_db), uid: str):
    user = crud.read_user(db, uid)
    zone = {}
    if user:
        zone = user.zone

    crud.delete_user(db, uid)

    if "latitude" in zone and "longitude" in zone:
        geo_tags = [f'latitude:{zone["latitude"]}', f'longitude:{zone["longitude"]}'] 
        statsd.decrement(metric="users.geo", tags=geo_tags.append("env:prod"))
    return {"message": "user deleted"}


@app.get("/users/{uid}/recommended", response_model=List[UserPublic])
def get_recommended(*, db: Session = Depends(get_db), uid: str):
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
def get_follow(*, db: Session = Depends(get_db), uid: str, otheruid: str):
    if not crud.read_follow(db, uid, otheruid):
        raise HTTPException(detail="follow does not exist", status_code=404)
    return {"message": "follow exists"}


@app.post("/users/{uid}/follows/{otheruid}")
def follow_user(*, db: Session = Depends(get_db), uid: str,
                      otheruid: str):
    crud.follow_user(db, uid, otheruid)
    return {"message": "follow added"}


@app.delete("/users/{uid}/follows/{otheruid}")
def unfollow_user(*, db: Session = Depends(get_db), uid, otheruid):
    crud.unfollow_user(db, uid, otheruid)
    return {"message": "follow removed"}

