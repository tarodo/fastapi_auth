import uvicorn
from fastapi import FastAPI

from app.api import users
from app.db import create_db_and_tables


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(users.router, prefix="/users", tags=["users"])
    return application


app = create_application()


@app.get("/")
def hello():
    return "Hi!"


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
