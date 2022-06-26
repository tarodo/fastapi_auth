from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.core.config import settings

engine = create_engine(settings.DB_URL, echo=True)
session = Session(bind=engine)
SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
