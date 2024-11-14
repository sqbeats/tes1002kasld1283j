import time

from endpoints.palindrome import PalindromeAPI

# Константы для тестов
valid_id: str = "371364c1-b9a9-442d-af11-8bddde012163"
invalid_id = "93bf9318-e36b-4fc0-b978-64d3264807b5"

class TestPalindromeAPI:

    def test_post_palindrome_request_true(self, api_client: PalindromeAPI):
        """Тест для POST /palindrome с параметром palindrome=True"""
        start_time = time.time()
        response = api_client.post_palindrome_request(is_palindrome=True)
        end_time = time.time()

        assert response is not None, "Ответ не должен быть None"
        assert "id" in response, "Ответ должен содержать 'id'"
        assert "result" in response, "Ответ должен содержать 'result'"
        assert isinstance(response["id"], str), "'id' должен быть строкой"
        assert isinstance(response["result"], str), "'result' должен быть строкой"
        assert response["result"] == response["result"][::-1], "'result' должен быть палиндромом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_post_palindrome_request_false(self, api_client: PalindromeAPI):
        """Тест для POST /palindrome с параметром palindrome=False"""
        start_time = time.time()
        response = api_client.post_palindrome_request(is_palindrome=False)
        end_time = time.time()

        assert response is not None, "Ответ не должен быть None"
        assert "id" in response, "Ответ должен содержать 'id'"
        assert "result" in response, "Ответ должен содержать 'result'"
        assert isinstance(response["id"], str), "'id' должен быть строкой"
        assert isinstance(response["result"], str), "'result' должен быть строкой"
        assert response["result"] != response["result"][::-1], "'result' не должен быть палиндромом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_get_result_by_id_valid(self, api_client: PalindromeAPI):
        """Тест для GET /palindrome/{id} с валидным id"""
        # Создаем палиндром для получения валидного ID
        post_response = api_client.post_palindrome_request(is_palindrome=True)
        assert post_response is not None, "Ответ POST запроса не должен быть None"
        result_id = post_response["id"]

        # Проверяем получение результата по валидному ID
        start_time = time.time()
        get_response = api_client.get_result_by_id(result_id)
        end_time = time.time()

        assert get_response is not None, "Ответ GET запроса не должен быть None"
        assert "result" in get_response, "Ответ должен содержать 'result'"
        assert get_response["result"] == post_response["result"], "Возвращаемый 'result' должен совпадать с оригиналом"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_get_result_by_invalid_id(self, api_client: PalindromeAPI):
        """Тест для GET /palindrome/{id} с невалидным id"""
        start_time = time.time()
        response = api_client.get_result_by_id(invalid_id)
        end_time = time.time()

        assert response is None, "Ответ должен быть None для невалидного ID"
        assert (end_time - start_time) < 0.5, "Время выполнения запроса должно быть меньше 500 мс"

    def test_post_palindrome_request_error_handling(self, api_client: PalindromeAPI, mocker):
        """Тест обработки ошибок в методе post_palindrome_request"""
        mocker.patch('requests.post', side_effect=Exception("Network error"))

        response = api_client.post_palindrome_request(is_palindrome=True)

        assert response is None, "Не ждем ответа, так как нет интернета"

