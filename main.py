import os

import uvicorn
from environs import Env
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import Session, SQLModel, create_engine, select

from models import User, UserIn, UserOut, responses

env = Env()
env.read_env()

app = FastAPI()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True)
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def hello():
    return "Hi!"


@app.post("/users/", tags=["users"], response_model=UserOut, status_code=200, responses=responses)
def create_user(payload: UserIn) -> User | JSONResponse:
    """Create One User"""
    users = select(User).where(User.email == payload.email)
    users = session.exec(users)
    for user in users:
        return JSONResponse(status_code=400, content={"err": "user_001", "message": "User exists"})
    user = User(**payload.dict())
    session.add(user)
    session.commit()
    return user


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=2)
