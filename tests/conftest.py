import os

import pytest


@pytest.fixture
def mock_api_data(mocker, requests_mock):
    def inner(api_data: dict):
        token = "fake_token"
        os.environ["SUPERHERO_API_TOKEN"] = token

        mocker.patch(
            "max_height_code.max_height.FIRST_HERO_NUMBER", min(api_data)
        )
        mocker.patch(
            "max_height_code.max_height.LAST_HERO_NUMBER", max(api_data)
        )

        for hero_id, data in api_data.items():
            url = f"https://www.superheroapi.com/api.php/{token}/{hero_id}"
            requests_mock.get(url, json=data)
    return inner
