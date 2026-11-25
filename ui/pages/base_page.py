"""Базовый Page Object."""
from typing import Optional

from playwright.sync_api import Page


class BasePage:
    """Общие действия и свойства для всех страниц."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.url: str = "https://www.kinopoisk.ru/"

    def open(self, url: Optional[str] = None) -> "BasePage":
        """Открывает страницу и ждёт загрузки DOM."""
        self.page.goto(url or self.url, wait_until="domcontentloaded")
        return self

    @property
    def title(self) -> str:
        """Возвращает заголовок текущей страницы."""
        return self.page.title()
