from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_users_normal_user_me(
    client: TestClient, user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"/users/me", headers=user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_admin"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER