from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.DB_URL, echo=True)
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
