import os

import uvicorn
from environs import Env
from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine

from models import User, UserIn, UserOut

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


@app.post("/users/", tags=["users"], response_model=UserOut, status_code=200)
def create_user(payload: UserIn) -> User:
    """Create User"""
    user = User(email=payload.email, password=payload.password)
    session.add(user)
    session.commit()
    return user


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8000)
