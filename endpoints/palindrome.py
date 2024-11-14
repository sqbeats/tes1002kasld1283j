from typing import Optional, Dict, Any

import requests

class PalindromeAPI:
    def __init__(self, base_url, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {}

    def post_palindrome_request(self, is_palindrome: bool) -> Optional[Dict[str, Any]]:
        """
        params:
        is_palindrome (bool): True - вернуть палиндром, False - вернуть не палиндром.

        response:
        {
            id(UUID),
            result: str
        }
        """

        try:
            response = requests.post(f"{self.base_url}/palindrome", json={"palindrome": is_palindrome})
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f"Error: {err}")
            return None

    def get_result_by_id(self, result_id: str) -> Optional[Dict[str, str]]:
        """
        params:
        - result_id: str ID результата.

        response:
        {
            result: str
        }
        """

        try:
            response = requests.get(f"{self.base_url}/palindrome/{result_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f"Error: {err}")
            return None
