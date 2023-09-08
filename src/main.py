from fastapi import FastAPI

app = FastAPI()

async def not_impl():
	return {msg: "Not yet implemented"} 

app.get("/users")(not_impl)
app.post("/users")(not_impl)
