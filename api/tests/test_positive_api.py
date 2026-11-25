"""Позитивные API-тесты: автоматизация кейсов API-01 — API-04."""
import allure
import pytest

from api.client import KinopoiskClient

INTERSTELLAR_ID = 252559

pytestmark = pytest.mark.api


def _doc_ids(payload: dict) -> list:
    """Возвращает список id из ответа с проверкой структуры."""
    docs = payload.get("docs")
    assert isinstance(docs, list), "docs должен быть списком"
    return docs


@allure.epic("API kinopoisk.dev")
@allure.feature("Позитивные сценарии")
class TestApiPositive:

    @allure.title("API-01: поиск фильмов с фильтрами (год, жанр, рейтинг)")
    @pytest.mark.parametrize("year", [2019, 2020])
    def test_search_with_filters(
        self, api_client: KinopoiskClient, year: int
    ) -> None:
        response = api_client.get_movies({
            "limit": 5,
            "year": year,
            "genres.name": "драма",
            "rating.kp": "7-10",
        })
        assert response.status_code == 200
        payload = response.json()
        docs = _doc_ids(payload)
        assert docs, "Список фильмов не должен быть пустым"
        for movie in docs:
            assert movie["year"] == year, f"Год {movie['year']} != {year}"
            rating = movie["rating"]["kp"]
            assert rating >= 7, f"Рейтинг {rating} ниже 7"
            assert rating <= 10, f"Рейтинг {rating} выше 10"
            genres = [genre["name"] for genre in movie["genres"]]
            assert "драма" in genres, f"Жанра драма нет: {genres}"

    @allure.title("API-02: поиск фильма по названию")
    def test_search_by_name(self, api_client: KinopoiskClient) -> None:
        response = api_client.search_movies("Интерстеллар")
        assert response.status_code == 200
        docs = _doc_ids(response.json())
        assert docs, "Поиск не вернул результатов"
        names = [str(movie.get("name", "")) for movie in docs]
        assert any(
            "Интерстеллар" in name for name in names
        ), f"Фильм не найден: {names}"

    @allure.title("API-03: получение фильма по известному ID")
    def test_get_movie_by_id(self, api_client: KinopoiskClient) -> None:
        response = api_client.get_movie(INTERSTELLAR_ID)
        assert response.status_code == 200
        movie = response.json()
        assert movie["id"] == INTERSTELLAR_ID, "Вернулся другой фильм"
        assert movie.get("name"), "Поле name отсутствует"
        assert movie.get("year"), "Поле year отсутствует"

    @allure.title("API-04: получение случайного фильма")
    def test_get_random_movie(self, api_client: KinopoiskClient) -> None:
        response = api_client.get_random_movie()
        assert response.status_code == 200
        movie = response.json()
        assert isinstance(movie, dict), "Должен вернуться объект, а не массив"
        assert movie.get("id"), "Поле id пустое"
