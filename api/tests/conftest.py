"""Фикстуры для API-тестов."""
import pytest

from api.client import KinopoiskClient
from config.settings import load_api_config


@pytest.fixture(scope="session")
def api_client() -> KinopoiskClient:
    """Клиент API с валидным токеном из .env."""
    config = load_api_config()
    if not config.api_key:
        pytest.skip("KINOPOISK_TOKEN не задан в .env")
    return KinopoiskClient(
        base_url=config.base_url,
        api_key=config.api_key,
        timeout=config.timeout,
    )
