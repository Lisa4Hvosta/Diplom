"""UI-тесты Кинопоиска: пять ключевых функциональных сценариев."""
import re
import allure
import pytest
from playwright.sync_api import expect

from ui.pages.home_page import HomePage
from ui.pages.search_page import SearchPage

pytestmark = pytest.mark.ui

GIBBERISH_QUERY = "qzxjkw9999zzzюу"
INTERSTELLAR_URL = "https://www.kinopoisk.ru/film/252559/"


@allure.epic("UI Кинопоиск")
class TestUiKinopoisk:

    @allure.title("UI-1: главная страница открывается")
    def test_home_page_title(self, home_page: HomePage) -> None:
        home_page.open()
        expect(home_page.page).to_have_title(re.compile("Кинопоиск"))

    @allure.title("UI-2: поиск с главной страницы ведёт к результатам")
    def test_search_from_main_page(self, home_page: HomePage) -> None:
        search_page: SearchPage = home_page.open().search("Интерстеллар")
        expect(search_page.page).to_have_url(re.compile("search"))
        search_page.expect_results_present()

    @allure.title("UI-3: страница фильма открывается по прямой ссылке")
    def test_movie_page_opens(self, home_page: HomePage) -> None:
        home_page.open(INTERSTELLAR_URL)
        expect(home_page.page).to_have_title(re.compile("Интерстеллар", re.I))

    @allure.title("UI-4: раздел сериалов открывается")
    def test_series_section(self, home_page: HomePage) -> None:
        home_page.open("https://www.kinopoisk.ru/series/")
        expect(home_page.page).to_have_title(re.compile("Сериалы", re.I))

    @allure.title("UI-5: поиск несуществующего запроса даёт пустой результат")
    def test_search_no_results(self, search_page: SearchPage) -> None:
        search_page.open_with_query(GIBBERISH_QUERY)
        search_page.expect_no_results()

    @allure.title("UI-6: на главной есть блок с карточками фильмов")
    def test_main_page_shows_movies(self, home_page: HomePage) -> None:
        home_page.open()
        expect(home_page.page.locator('a[href^="/film/"]').first).to_be_visible()
