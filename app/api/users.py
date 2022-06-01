from enum import Enum

from fastapi import APIRouter
from sqlmodel import select

from app.api.tools import raise_400
from app.db import session
from app.models import User, UserIn, UserOut, responses

router = APIRouter()


class UsersErrors(Enum):
    UserWithEmailExists = "User with Email exists"


@router.post("/", response_model=UserOut, status_code=200, responses=responses)
def create_user(payload: UserIn) -> User:
    """Create One User"""
    users = select(User).where(User.email == payload.email)
    users = session.exec(users).one_or_none()
    if users:
        raise_400(UsersErrors.UserWithEmailExists)

    user = User(**payload.dict())
    session.add(user)
    session.commit()
    return user
