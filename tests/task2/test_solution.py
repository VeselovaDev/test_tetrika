import requests
from bs4 import BeautifulSoup

from task2.solution import BASE_URL, START_URL, get_animals, get_next_url
from tests.task2.conftest import NEXT_URL


def test_get_next_url_raw():
    page = requests.get(BASE_URL + START_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    res = get_next_url(soup)
    assert res == NEXT_URL


def test_get_animals():
    page = requests.get(BASE_URL + START_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    res = get_animals(soup)
    assert "Аардоникс" in res
    assert len(res) == 200
