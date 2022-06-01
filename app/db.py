import os

from environs import Env
from sqlmodel import Session, SQLModel, create_engine

env = Env()
env.read_env()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True)
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
