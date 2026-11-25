"""Главная страница Кинопоиска."""
import re

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from ui.pages.base_page import BasePage
from ui.pages.search_page import SearchPage


class HomePage(BasePage):
    """Действия на главной странице kinopoisk.ru."""

    URL: str = "https://www.kinopoisk.ru/"
    SEARCH_INPUT: str = 'input[name="keyword"]'
    COOKIE_BUTTON: str = 'button:has-text("Принять")'

    def open(self) -> "HomePage":
        self.page.goto(self.URL, wait_until="domcontentloaded")
        self._dismiss_cookies()
        return self

    def search(self, query: str) -> SearchPage:
        """Вводит запрос в поисковую строку и отправляет его."""
        field = self.page.locator(self.SEARCH_INPUT).first
        expect(field).to_be_visible()
        field.fill(query)
        self.page.keyboard.press("Enter")
        return SearchPage(self.page)

    def _dismiss_cookies(self) -> None:
        """Принимает cookie-баннер, если он появился (без sleep)."""
        try:
            self.page.locator(self.COOKIE_BUTTON).first.click(timeout=3000)
        except PlaywrightTimeoutError:
            pass
