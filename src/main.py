from fastapi import FastAPI

app = FastAPI()

async def not_impl():
	return {"message": "Not yet implemented"} 


@app.get("/")
async def root():
	return {"message": "Users microsevice"}

app.get("/users")(not_impl)
app.post("/users")(not_impl)
