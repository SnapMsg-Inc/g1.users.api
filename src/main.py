from fastapi import FastAPI

import psycopg2


app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Users microsevice"}

con = psycopg2.connect(
	database="usersdb",
	user="snapmsg",
	password="1234",
	host="users-db",
	port= '5432'
)
#
#    Users routes
#
#app.get("/users")(users.get_users)
#app.post("/users")(users.create_users)


