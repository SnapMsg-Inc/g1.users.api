from fastapi import FastAPI

# import users

import psycopg2


app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Users microsevice"}

@app.get("/users")
async def getUsers():
	return {"message": "get users"}

# con = psycopg2.connect(
# 	database="usersdb",
# 	user="snapmsg",
# 	password=1234,
# 	host="users-db",
# 	port= '5432'
# )

# app.get("/users")(users.get_users)
# app.post("/users")(users.create_users)


