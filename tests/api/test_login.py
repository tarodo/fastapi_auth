from sqlmodel import Session
from starlette.testclient import TestClient

from app.api.login import LoginErrors
from app.crud import users
from app.models import UserIn
from tests.utils.utils import random_email, random_lower_string


def test_get_access_token(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    users.create(db, payload=user_in)
    data = {"username": email, "password": password}
    r = client.post(f"/login/access-token", data=data)
    token = r.json()
    assert r.status_code == 200
    assert "access_token" in token
    assert token["access_token"]
    assert "token_type" in token
    assert token["token_type"] == "bearer"


def test_get_access_token_wrong_creds(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"username": email, "password": password}
    r = client.post(f"/login/access-token", data=data)
    token = r.json()
    assert r.status_code == 400
    assert token["detail"]["err"] == str(LoginErrors.IncorrectCredentials)
