"""Страница результатов поиска."""
import re
from urllib.parse import quote

from playwright.sync_api import expect

from ui.pages.base_page import BasePage


class SearchPage(BasePage):
    """Страница /search/?text=... на kinopoisk.ru."""

    URL: str = "https://www.kinopoisk.ru/search/"

    def open_with_query(self, query: str) -> "SearchPage":
        """Открывает страницу поиска с заданным запросом."""
        url = f"{self.URL}?text={quote(query)}"
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    def expect_results_present(self) -> None:
        """Ожидает, что в выдаче есть хотя бы один фильм."""
        expect(self.page.locator('a[href^="/film/"]').first).to_be_visible()

    def expect_no_results(self) -> None:
        """Ожидает сообщение об отсутствии результатов."""
        empty = self.page.get_by_text(
            re.compile("ничего не найд|не нашлось", re.I)
        )
        expect(empty.first).to_be_visible()
