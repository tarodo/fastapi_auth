from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.core.security import verify_password
from app.crud import users
from app.models import UserIn, UserUpdate
from tests.utils.utils import random_email, random_lower_string


def test_user_create(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, payload=user_in)
    assert user.email == email
    assert hasattr(user, "password")
    assert user.is_admin is False


def test_admin_create(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password, is_admin=True)
    user = users.create(db, payload=user_in)
    assert user.email == email
    assert hasattr(user, "password")
    assert user.is_admin is True


def test_user_authenticate(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, payload=user_in)
    authenticated_user = users.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_user_not_authenticate(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = users.authenticate(db, email=email, password=password)
    assert user is None


def test_user_not_authenticate_wrong_pass(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, payload=user_in)
    wrong_password = random_lower_string()
    user_test = users.authenticate(db, email=user.email, password=wrong_password)
    assert user_test is None


def test_user_read_by_id(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, user_in)
    user_test = users.read_by_id(db, user.id)
    assert user_test
    assert user.email == user_test.email
    assert jsonable_encoder(user) == jsonable_encoder(user_test)


def test_user_read_by_wrong_id(db: Session) -> None:
    user_test = users.read_by_id(db, 666)
    assert not user_test


def test_user_read_by_email(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, user_in)
    user_test = users.read_by_email(db, user.email)
    assert user_test
    assert user.email == user_test.email
    assert jsonable_encoder(user) == jsonable_encoder(user_test)


def test_user_read_by_wrong_email(db: Session) -> None:
    user_test = users.read_by_email(db, random_email())
    assert not user_test


def test_user_update_password(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password)
    user = users.create(db, payload=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password)
    users.update(db, user, payload=user_in_update)
    user_test = users.read_by_id(db, user.id)
    assert user_test
    assert user.email == user_test.email
    assert verify_password(new_password, user_test.password)


def test_user_update_is_admin(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password, is_admin=False)
    user = users.create(db, payload=user_in)
    user_in_update = UserUpdate(is_admin=True)
    users.update(db, user, payload=user_in_update)
    user_test = users.read_by_id(db, user.id)
    assert user_test
    assert user.email == user_test.email
    assert user.is_admin


def test_remove_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserIn(email=email, password=password, is_admin=False)
    user = users.create(db, payload=user_in)
    user_remove = users.remove(db, user)
    user_test = users.read_by_id(db, user.id)
    assert not user_test
    assert user_remove == user
