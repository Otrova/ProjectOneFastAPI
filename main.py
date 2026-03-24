from fastapi import FastAPI
from routers import users, products


app = FastAPI()

app.include_router(users.routerUsers)

@app.get("/")
async def root():
    return "root"