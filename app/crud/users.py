from app.models import User, UserIn
from sqlmodel import select
from app.db import session
from fastapi.encoders import jsonable_encoder


def read_by_email(email: str) -> User | None:
    """Read one user by email"""
    user = select(User).where(User.email == email)
    user = session.exec(user).one_or_none()
    return user


def create(payload: UserIn) -> User:
    """Create user"""
    user = User(**jsonable_encoder(payload))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
