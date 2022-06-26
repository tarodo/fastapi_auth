from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.users import UsersErrors
from app.core.config import settings
from app.crud import users
from app.models import UserIn
from tests.utils.utils import random_email, random_lower_string


def test_get_users_normal_user_me(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"/users/me", headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_admin"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_unauth_user(client: TestClient) -> None:
    r = client.get(f"/users/me", headers={})
    assert r.status_code == 401


def test_create_user_new_email(
    client: TestClient, user_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"/users/", headers=user_token_headers, json=data)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = users.read_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


def test_create_user_existing_email(
    client: TestClient, user_token_headers: dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    users.create(db, payload=user_in)
    data = {"email": email, "password": password}
    r = client.post(f"/users/", headers=user_token_headers, json=data)
    created_user = r.json()
    assert r.status_code == 400
    assert created_user["detail"]["err"] == str(UsersErrors.UserWithEmailExists)
