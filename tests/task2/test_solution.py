import csv
import os

import pytest
import requests
from bs4 import BeautifulSoup, element
from requests.exceptions import MissingSchema

from task2.solution import (
    ORIGINE_AND_HOSTNAME,
    RUSSIAN_ALPHABET,
    append_wiki_hostname,
    count_animals_per_letter,
    get_animals_list,
    get_link_to_current_page_from_csv,
    get_link_to_next_page_from_tag,
    get_pathname_and_query,
    get_previous_count_of_animals,
    get_soup,
    save_beasts,
    save_next_link_to_file,
)
from tests.task2.conftest import ANIMALS, START_URL, TEST_FILE


def test_get_link_to_current_page_from_csv_no_previous_link(tear_down):
    """Проверяю, что мой метод не возвращает ссылки, если она не записана в файл"""

    # создаю пустой файл, чтобы проверить, что будет, если у меня нет ссылки на следующую страницу
    with open(TEST_FILE, "w"):
        url = get_link_to_current_page_from_csv(link_in_scv=TEST_FILE)
    assert not url


def test_get_link_to_current_page_from_csv_with_previous_link(tear_down):
    """Проверяю, что я считываю из файла ссылку на текущую страницу"""

    # Создаю пустой файл, чтобы проверить случай, когда
    # у меня есть ссылка на следующую страницу
    with open(TEST_FILE, "w") as file:
        file.write(START_URL)
    url = get_link_to_current_page_from_csv(link_in_scv=TEST_FILE)
    assert url == START_URL


def test_get_soup_no_url():
    """Проверяю, что будет вызвана ошибка MissingSchema, если урла нет"""

    with pytest.raises(MissingSchema):
        get_soup("")


def test_get_soup():
    """Проверяю, что я получаю объект BeautifulSoup из урла"""

    res = get_soup("https://ru.wikipedia.org/wiki/Заглавная_страница")
    assert isinstance(res, BeautifulSoup)


def test_get_link_to_next_page_from_tag():
    """Проверяю, что я нахожу ссылки на следующие страницы в диве"""

    soup = get_soup(START_URL)
    page_content = soup.find("div", id="mw-pages")
    res = get_link_to_next_page_from_tag(page_content)
    assert isinstance(res, element.Tag)
    assert "Следующая страница" in res
    assert str(res) != START_URL


def test_get_pathname_and_query():
    """Проверяю, что из тэга BeautifulSoup достаётся путь и квери"""

    page = requests.get(START_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    page_content = soup.find("div", id="mw-pages")
    tag = [
        link for link in page_content.find_all("a") if link.text == "Следующая страница"
    ][0]

    res = get_pathname_and_query(tag)
    assert "</a>" not in res
    assert "/w/index.php?title=" in res
    assert "#mw-pages" in res
    assert "pagefrom=" in res


def test_append_wiki_hostname():
    """Проверяю, что метод добавляет доменное имя"""

    url = "our_awesome_url"
    res = append_wiki_hostname(url)
    assert res == ORIGINE_AND_HOSTNAME + url


def test_save_next_link_to_file_creates_file(tear_down):
    """Проверяю, что метод создаёт новый файл, если файла с переданным именем нет"""

    save_next_link_to_file(filename=TEST_FILE, url="Hello World")
    assert os.path.exists(TEST_FILE)


def test_save_next_link_to_file_creates_file(tear_down):
    """Проверяю, что метод записывает строку в файл"""
    url = "Hello World"
    save_next_link_to_file(filename=TEST_FILE, url=url)
    with open(TEST_FILE) as file:
        result = file.read()
    assert url in result


def test_get_animals_list():
    """Проверяю, что метод получает список животных"""
    page = requests.get(START_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    res = get_animals_list(soup)
    assert isinstance(res, list)
    # Википедия выдаёт по 200 животных на страницу
    assert len(res) == 200
    assert res[0].isalpha()
    assert res[0][0] in RUSSIAN_ALPHABET


def test_count_animals_per_letter():
    """Проверяю, что метод подсчитывает количество животных на каждую букву алфавита"""

    res = count_animals_per_letter(ANIMALS)
    assert res["Ч"] == 1
    assert res["П"] == 2
    assert res["Х"] == 1
    res.pop("Ч")
    res.pop("П")
    res.pop("Х")
    # проверяю, что у всех остальных букв в качестве значения указан ноль
    assert set(res.values()) == {0}


def test_get_previous_count_of_animals_no_previous_animals(tear_down):
    """Проверяю, что если животных нет, вернётся пустой словарь"""

    # создаю пустой файл
    filepath = TEST_FILE
    with open(filepath, "w"):
        pass
    res = get_previous_count_of_animals(filepath)
    assert res == {}


def test_get_previous_count_of_animals(tear_down):
    """Проверяю, что корректно считываю количество животных из файла"""

    # создаю пустой файл
    filepath = TEST_FILE
    res = {letter: 0 for letter in RUSSIAN_ALPHABET}
    # записываю в него количество животных на букву алфавита
    for animal in ANIMALS:
        res[animal[0]] += 1
    with open(filepath, "w") as file:
        for key, value in res.items():
            file.write(f"{key},{value}\n")
    # проверяю, что я корректно считываю из файла количество животных
    res = get_previous_count_of_animals(filepath)
    assert res["Ч"] == 1
    assert res["П"] == 2
    assert res["Х"] == 1
    res.pop("Ч")
    res.pop("П")
    res.pop("Х")
    # проверяю, что у всех остальных букв в качестве значения указан ноль
    assert set(res.values()) == {0}


def test_save_beasts(tear_down):
    """Проверяю, что корректно подсчитываю количество животных в текущей итерации
    и успешно сохраняю его в файл
    """

    previous_animals_count = {
        "А": 500,
        "Б": 0,
        "В": 0,
        "Г": 0,
        "Д": 0,
        "Е": 0,
        "Ё": 0,
        "Ж": 0,
        "З": 0,
        "И": 0,
        "Й": 0,
        "К": 0,
        "Л": 0,
        "М": 0,
        "Н": 0,
        "О": 0,
        "П": 0,
        "Р": 0,
        "С": 0,
        "Т": 0,
        "У": 0,
        "Ф": 0,
        "Х": 0,
        "Ц": 0,
        "Ч": 0,
        "Ш": 0,
        "Щ": 0,
        "Ъ": 0,
        "Ы": 0,
        "Ь": 0,
        "Э": 0,
        "Ю": 0,
        "Я": 0,
    }
    current_animals_count = {
        "А": 0,
        "Б": 600,
        "В": 0,
        "Г": 0,
        "Д": 0,
        "Е": 0,
        "Ё": 0,
        "Ж": 0,
        "З": 0,
        "И": 0,
        "Й": 0,
        "К": 0,
        "Л": 0,
        "М": 0,
        "Н": 0,
        "О": 0,
        "П": 0,
        "Р": 0,
        "С": 0,
        "Т": 0,
        "У": 0,
        "Ф": 0,
        "Х": 0,
        "Ц": 0,
        "Ч": 0,
        "Ш": 0,
        "Щ": 0,
        "Ъ": 0,
        "Ы": 0,
        "Ь": 0,
        "Э": 0,
        "Ю": 0,
        "Я": 0,
    }
    save_beasts(TEST_FILE, previous_animals_count, current_animals_count)
    # cчитать результат выполнения функции из файла
    with open(TEST_FILE, mode="r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        saved_res = {}
        for row in spamreader:
            # ключи и значения разделены запятой
            # в каждом ряду лежит список
            key, value = row[0].split(",")
            saved_res[key] = int(value)
    assert saved_res["А"] == 500
    assert saved_res["Б"] == 600
    saved_res.pop("А")
    saved_res.pop("Б")
    # проверяю, что у всех остальных букв в качестве значения указан ноль
    assert set(saved_res.values()) == {0}
