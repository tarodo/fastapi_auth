from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.crud import users
from app.models import User, UserIn, UserUpdate
from tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """Return headers for the creds"""
    data = {"username": email, "password": password}
    r = client.post(f"/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    """Return new user with random email and pass"""
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(username=email, email=email, password=password)
    user = users.create(db, user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = users.read_by_email(db, email=email)
    if not user:
        user_in_create = UserIn(username=email, email=email, password=password)
        user = users.create(db, user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = users.update(db, db_obj=user, payload=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
