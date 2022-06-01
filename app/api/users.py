from enum import Enum

from fastapi import APIRouter


from app.api.tools import raise_400
from app.crud import users
from app.models import User, UserIn, UserOut, responses

router = APIRouter()


class UsersErrors(Enum):
    UserWithEmailExists = "User with Email exists"


@router.post("/", response_model=UserOut, status_code=200, responses=responses)
def create_user(payload: UserIn) -> User:
    """Create One User"""
    old_user = users.read_by_email(payload.email)
    if old_user:
        raise_400(UsersErrors.UserWithEmailExists)

    user = users.create(payload)
    return user
