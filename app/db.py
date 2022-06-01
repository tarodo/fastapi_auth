from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.DB_URL, echo=True)
session = Session(bind=engine)
