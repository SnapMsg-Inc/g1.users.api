from fastapi import FastAPI
from dbconf import engine, Session
from models.user import Base, User
from routes import users
from sqlalchemy import MetaData

import psycopg2


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
	
	return {"message": "Users microsevice"}

#
#    Users routes
#
app.get("/users")(users.get_users)
app.post("/users/{uid}", status_code=201)(users.create_user)
app.patch("/users/{uid}")(users.update_user)
app.delete("/users/{uid}")(users.delete_user)

app.post("/users/{uid}/follow/{otheruid}")(users.follow_user)
app.delete("/users/{uid}/follow/{otheruid}")(users.unfollow_user)

app.get("/users/{uid}/recommended")(users.get_recommended)

