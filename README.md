1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/sqbeats/tes1002kasld1283j.git 
    cd tes1002kasld1283j
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Запустите тесты

   ```bash
   pytest tests/test_palindrome.py
