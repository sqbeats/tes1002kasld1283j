from endpoints.palindrome import PalindromeAPI

import pytest

base_url: str = "http://localhost:5000"

@pytest.fixture(scope="session")
def api_client():
    return PalindromeAPI(base_url=base_url, headers={"Authorization": "Bearer ---"})
