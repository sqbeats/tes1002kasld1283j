import uuid

def is_valid_uuid(uuid_to_test: str) -> bool:
    """Проверяет, что строка является валидным UUID."""
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False
