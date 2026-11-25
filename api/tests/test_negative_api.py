"""Негативные API-тесты: автоматизация кейсов API-05 — API-08."""
import allure
import pytest

from api.client import KinopoiskClient
from config.settings import load_api_config

pytestmark = pytest.mark.api


def _error_text(payload: dict) -> str:
    """Собирает текст ошибки независимо от формата поля message."""
    message = payload.get("message", "")
    if isinstance(message, list):
        return " ".join(str(item) for item in message)
    return str(message)


@allure.epic("API kinopoisk.dev")
@allure.feature("Негативные сценарии")
class TestApiNegative:

    @allure.title("API-05: запрос с невалидным токеном -> 401")
    def test_invalid_token_returns_401(self) -> None:
        config = load_api_config()
        client = KinopoiskClient(config.base_url, api_key="invalid_token_123")
        response = client.get_movies({"limit": 5})
        assert response.status_code == 401
        assert "docs" not in response.json(), "При 401 не должно быть данных"

    @allure.title("API-06: ID вне допустимого диапазона -> 400")
    @pytest.mark.parametrize("movie_id", [0, -1, 999999999])
    def test_movie_id_out_of_range(
        self, api_client: KinopoiskClient, movie_id: int
    ) -> None:
        response = api_client.get_movie(movie_id)
        assert response.status_code == 400
        assert "диапазоне" in _error_text(response.json())

    @allure.title("API-07: limit вне диапазона 1-250 -> 400")
    @pytest.mark.parametrize("limit", [0, 999])
    def test_limit_out_of_range(
        self, api_client: KinopoiskClient, limit: int
    ) -> None:
        response = api_client.get_movies({"limit": limit})
        assert response.status_code == 400
        assert "limit" in _error_text(response.json())

    @allure.title(
            "API-08: PATCH на эндпоинте списка отклоняется (баг №1 исправлен)"
        )
    def test_patch_method_rejected(self, api_client: KinopoiskClient) -> None:
        response = api_client.patch_movies({"limit": 5})
        assert response.status_code in (400, 404, 405)
