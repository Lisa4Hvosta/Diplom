"""API-клиент kinopoisk.dev (v1.4)."""
from typing import Any, Dict, Optional

import requests


class KinopoiskClient:
    """Обёртка над HTTP-запросами к API Кинопоиска."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        headers = {"X-API-KEY": api_key, "Accept": "application/json"}
        self._session.headers.update(headers)

    def set_api_key(self, api_key: str) -> None:
        """Подменяет токен — для негативных сценариев."""
        self._session.headers["X-API-KEY"] = api_key

    def get_movies(
        self, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """GET /v1.4/movie — список фильмов с фильтрами."""
        return self._request("GET", "/v1.4/movie", params=params)

    def search_movies(
        self, query: str, page: int = 1, limit: int = 5
    ) -> requests.Response:
        """GET /v1.4/movie/search — поиск по названию."""
        params = {"query": query, "page": page, "limit": limit}
        return self._request("GET", "/v1.4/movie/search", params=params)

    def get_movie(self, movie_id: int) -> requests.Response:
        """GET /v1.4/movie/{id} — фильм по идентификатору."""
        return self._request("GET", f"/v1.4/movie/{movie_id}")

    def get_random_movie(self) -> requests.Response:
        """GET /v1.4/movie/random — случайный фильм."""
        return self._request(
            "GET", "/v1.4/movie/random", params={"notNullFields": "id"}
        )

    def patch_movies(
        self, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """PATCH /v1.4/movie — проверка исправленного бага №1."""
        return self._request("PATCH", "/v1.4/movie", params=params)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Выполняет запрос и возвращает ответ без исключений."""
        url = f"{self._base_url}{path}"
        return self._session.request(
            method, url, params=params, timeout=self._timeout
        )
