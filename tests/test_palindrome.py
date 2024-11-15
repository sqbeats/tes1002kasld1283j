import time
from unittest.mock import MagicMock

from endpoints.palindrome import PalindromeAPI
from utils.validators import is_valid_uuid

# Константы для тестов
valid_id: str = "371364c1-b9a9-442d-af11-8bddde012163"
invalid_id = "93bf9318-e36b-4fc0-b978-64d3264807b5"


class TestPalindromeAPI:

    def test_post_palindrome_request_true(self, api_client: PalindromeAPI, mocker):
        """Тест для POST /palindrome с параметром palindrome=True"""
        mock_response = {"id": "c44f1d25-f696-498f-b241-005d0d0e0c30", "result": "madam"}
        mock_post = mocker.patch(
            'requests.post',
            return_value=MagicMock(json=lambda: mock_response, status_code=200)
        )

        start_time = time.time()
        response = api_client.post_palindrome_request(is_palindrome=True)
        end_time = time.time()

        mock_post.assert_called_once()
        assert mock_post.return_value.status_code == 200, "Статус код должен быть 200"

        assert response is not None, "Ответ не должен быть None"
        assert "id" in response, "Ответ должен содержать 'id'"
        assert "result" in response, "Ответ должен содержать 'result'"
        assert is_valid_uuid(response["id"]), "'id' должен быть валидным UUID"
        assert isinstance(response["result"], str), "'result' должен быть строкой"
        assert response["result"] == response["result"][::-1], "'result' должен быть палиндромом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_post_palindrome_request_false(self, api_client: PalindromeAPI, mocker):
        """Тест для POST /palindrome с параметром palindrome=False"""
        mock_response = {"id": "c44f1d25-f696-498f-b241-005d0d0e0c30", "result": "hello"}
        mock_post = mocker.patch(
            'requests.post',
            return_value=MagicMock(json=lambda: mock_response, status_code=200)
        )

        start_time = time.time()
        response = api_client.post_palindrome_request(is_palindrome=False)
        end_time = time.time()

        mock_post.assert_called_once()
        assert mock_post.return_value.status_code == 200, "Статус код должен быть 200"

        assert response is not None, "Ответ не должен быть None"
        assert "id" in response, "Ответ должен содержать 'id'"
        assert "result" in response, "Ответ должен содержать 'result'"
        assert is_valid_uuid(response["id"]), "'id' должен быть валидным UUID"
        assert isinstance(response["result"], str), "'result' должен быть строкой"
        assert response["result"] != response["result"][::-1], "'result' не должен быть палиндромом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_get_result_by_id_valid(self, api_client: PalindromeAPI, mocker):
        """Тест для GET /palindrome/{id} с валидным id"""
        mock_post_response = {"id": valid_id, "result": "madam"}
        mock_get_response = {"result": "madam"}

        mock_post = mocker.patch(
            'requests.post',
            return_value=MagicMock(json=lambda: mock_post_response, status_code=200)
        )
        mock_get = mocker.patch(
            'requests.get',
            return_value=MagicMock(json=lambda: mock_get_response, status_code=200)
        )

        # Создаем палиндром для получения валидного ID
        post_response = api_client.post_palindrome_request(is_palindrome=True)
        assert post_response is not None, "Ответ POST запроса не должен быть None"
        result_id = post_response["id"]

        # Проверяем получение результата по валидному ID
        start_time = time.time()
        get_response = api_client.get_result_by_id(result_id)
        end_time = time.time()

        mock_post.assert_called_once()
        assert mock_post.return_value.status_code == 200, "Статус код для POST запроса должен быть 200"

        mock_get.assert_called_once_with(f"{api_client.base_url}/palindrome/{result_id}")
        assert mock_get.return_value.status_code == 200, "Статус код для GET запроса должен быть 200"

        assert is_valid_uuid(result_id), "'id' должен быть валидным UUID"
        assert get_response is not None, "Ответ GET запроса не должен быть None"
        assert "result" in get_response, "Ответ должен содержать 'result'"
        assert get_response["result"] == post_response["result"], "Возвращаемый 'result' должен совпадать с оригиналом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_get_result_by_invalid_id(self, api_client: PalindromeAPI, mocker):
        """Тест для GET /palindrome/{id} с невалидным id"""
        mock_get = mocker.patch(
            'requests.get',
            return_value=MagicMock(status_code=404)
        )

        start_time = time.time()
        response = api_client.get_result_by_id(invalid_id)
        end_time = time.time()

        mock_get.assert_called_once_with(f"{api_client.base_url}/palindrome/{invalid_id}")
        assert mock_get.return_value.status_code == 404, "Статус код для GET запроса с невалидным ID должен быть 404"
        assert response is not None, "Ответ не должен быть None для невалидного ID"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_post_palindrome_request_error_handling(self, api_client: PalindromeAPI, mocker):
        """Тест обработки ошибок в методе post_palindrome_request"""
        mocker.patch('requests.post', side_effect=Exception("Network error"))

        response = api_client.post_palindrome_request(is_palindrome=True)

        assert response is None, "Не ждем ответа, так как нет интернета"

