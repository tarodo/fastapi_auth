from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import select

from app.db import session
from app.models import User, UserIn, UserOut, responses

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=200, responses=responses)
def create_user(payload: UserIn) -> User | JSONResponse:
    """Create One User"""
    users = select(User).where(User.email == payload.email)
    users = session.exec(users)
    for user in users:
        return JSONResponse(
            status_code=400, content={"err": "user_001", "message": "User exists"}
        )
    user = User(**payload.dict())
    session.add(user)
    session.commit()
    return user
