"""Фикстуры для UI-тестов (page приходит из pytest-playwright)."""
import pytest
from playwright.sync_api import Page

from ui.pages.home_page import HomePage
from ui.pages.search_page import SearchPage


@pytest.fixture()
def home_page(page: Page) -> HomePage:
    """Свежая главная страница для каждого теста."""
    return HomePage(page)


@pytest.fixture()
def search_page(page: Page) -> SearchPage:
    """Свежая страница поиска для каждого теста."""
    return SearchPage(page)
