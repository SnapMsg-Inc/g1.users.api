from fastapi import FastAPI
from routes import users
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
app.get("/users")(users.get_users)
app.post("/users/{uid}")(users.create_users, status_code=201)
app.patch("/users/{uid}")(users.update_user)
app.delete("/users/{uid}")(users.delete_user)

app.post("/users/{uid}/follow/{otheruid}", users.follow_user)
app.delete("/users/{uid}/follow/{otheruid}", users.unfollow_user)

app.get("/users/recommended")(users.get_recommended)

