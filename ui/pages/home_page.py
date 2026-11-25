"""Главная страница Кинопоиска."""
from typing import Optional

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    expect,
)

from ui.pages.base_page import BasePage
from ui.pages.search_page import SearchPage


class HomePage(BasePage):
    """Действия на главной странице kinopoisk.ru."""

    URL: str = "https://www.kinopoisk.ru/"
    SEARCH_INPUT: str = '[aria-label="Фильмы, сериалы, персоны"]'
    CLOSE_DIALOG_BUTTON: str = '[aria-label="Закрыть коммуникацию"]'

    def open(self, url: Optional[str] = None) -> "HomePage":
        """Открывает страницу и закрывает всплывающие окна."""
        self.page.goto(url or self.URL, wait_until="domcontentloaded")
        self._dismiss_dialogs()
        return self

    def search(self, query: str) -> SearchPage:
        """Вводит запрос в поисковую строку и отправляет его."""
        field = self.page.get_by_role("combobox")
        expect(field).to_be_visible()
        field.fill(query)
        self.page.keyboard.press("Enter")
        return SearchPage(self.page)

    def _dismiss_dialogs(self) -> None:
        """Закрывает диалог, если он появился (без sleep)."""
        try:
            self.page.locator(self.CLOSE_DIALOG_BUTTON).first.click(
                timeout=3000
            )
        except PlaywrightTimeoutError:
            pass
