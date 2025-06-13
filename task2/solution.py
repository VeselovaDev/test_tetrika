import csv
from pathlib import Path
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup, element

RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
NEXT_URL_FILE = Path(__file__).parent / "next_link.csv"
RESULT_FILE = Path(__file__).parent / "beasts.csv"
BASE_URL = "https://ru.wikipedia.org"
START_URL = "/wiki/Категория:Животные_по_алфавиту"


def get_current_url() -> str:
    try:
        with open(NEXT_URL_FILE, mode="r") as file:
            url = file.read()
            return url
    except FileNotFoundError:
        return BASE_URL + START_URL


def get_soup(url) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_next_url_raw(page_content: element.Tag) -> element.Tag:
    return [
        link for link in page_content.find_all("a") if link.text == "Следующая страница"
    ][0]["href"]


def get_next_url(soup) -> str:
    next_url_div = soup.find("div", id="mw-pages")
    return BASE_URL + unquote(get_next_url_raw(next_url_div))


def save_next_url(url: str) -> None:
    with open(NEXT_URL_FILE, mode="w") as file:
        file.write(url)


def get_animals(soup: BeautifulSoup) -> list[str]:
    page_content = soup.find("div", class_="mw-category mw-category-columns")
    return [link.text for link in page_content.find_all("a")]


def get_container_for_result() -> dict[str, int]:
    return {letter: 0 for letter in RUSSIAN_ALPHABET}


def get_animals_from_file() -> dict[str, int]:
    try:
        with open(RESULT_FILE, mode="r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            animals_from_file = {}
            for row in spamreader:
                letter, count = row[0].split(",")
                animals_from_file[letter] = int(count)
            return animals_from_file

    except FileNotFoundError:
        return get_container_for_result()


def update_result(
    current_result: dict[str, int], new_animals: dict[str, int]
) -> dict[str, int]:
    for animal in new_animals:
        try:
            current_result[animal[0]] += 1
        # Some animal names are in latin letters; skip them as per the task
        except KeyError:
            continue
    return current_result


def sum_results(new: list[str], old: dict[str, int]) -> dict[str, int]:
    return {animal: old[animal] + new[animal] for animal in old.keys()}


def transform_list_to_dict(animals: list[str]) -> dict[str, int]:
    res = get_container_for_result()
    for animal in animals:
        res[animal[0]] += 1
    return res


def save_animals(current_result: list[str]) -> None:
    saved_result = get_animals_from_file()
    add_to_result = transform_list_to_dict(current_result)

    write_this = sum_results(add_to_result, saved_result)

    with open(RESULT_FILE, mode="w+") as file:
        for key, value in write_this.items():
            file.write(f"{key},{value}\n")


def scrap_current_url(current_url: str) -> tuple[str, list[str]]:
    soup = get_soup(current_url)
    next_url = get_next_url(soup)
    animals = get_animals(soup)
    return next_url, animals


def scrap_animals_list():
    current_url = get_current_url()
    next_url, animals = scrap_current_url(current_url)
    save_next_url(next_url)
    save_animals(animals)


if __name__ == "__main__":
    scrap_animals_list()
