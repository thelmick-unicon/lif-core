from typing import Optional

from deepdiff import DeepDiff
from httpx import AsyncClient


async def login_user_to_lif_advisor(
    *, client: AsyncClient, username: str, password: str, expected_response: Optional[dict] = None
) -> dict:
    """
    Logs a user into LIF Advisor.

    If expected_response is provided, the login response will be compared to it, adding in the access_token and refresh_token.

    Returns the login response JSON.
    """
    details = {"username": username, "password": password}
    response = await client.post("/login", json=details)
    assert response.status_code == 200, response
    response_json = response.json()
    assert isinstance(response_json.get("access_token"), str)
    assert isinstance(response_json.get("refresh_token"), str)
    if expected_response:
        expected_response["access_token"] = response_json.get("access_token")
        expected_response["refresh_token"] = response_json.get("refresh_token")
        diff = DeepDiff(expected_response, response_json)
        assert not diff, diff  # prints out the differences if any

    return response_json


async def logout_user_from_lif_advisor(
    *, client: AsyncClient, access_token: str, expected_response: Optional[dict] = None
) -> dict:
    """
    Logs a user out of LIF Advisor.

    If expected_response is provided, the logout response will be compared to it.

    Returns the logout response JSON.
    """

    auth_headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/logout", headers=auth_headers)
    response_json = response.json()
    assert response.status_code == 200, response.text

    if expected_response:
        diff = DeepDiff(expected_response, response_json)
        assert not diff, diff  # prints out the differences if any

    return response_json
