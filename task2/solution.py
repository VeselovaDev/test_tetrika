import csv
import requests

from urllib.parse import unquote
from bs4 import BeautifulSoup, element


RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
NEXT_LINK_SCV = "task2/next_link.csv"
RESULT_FILE = "task2/beasts.csv"
ORIGINE_AND_HOSTNAME = "https://ru.wikipedia.org"


def get_link_to_current_page_from_csv(link_in_scv: str) -> str:
    """Получаю ссылку на текущую страницу"""
    with open(link_in_scv, mode="r") as file:
        url = file.read()
    return url


def get_soup(url) -> BeautifulSoup:
    """Получаю объект BeautifulSoup"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_link_to_next_page_from_tag(page_content: element.Tag) -> element.Tag:
    """Получаю ссылку на следующую страницу"""
    return [
        link for link in page_content.find_all("a") if link.text == "Следующая страница"
    ][0]


def get_pathname_and_query(encoded_next_link_tag: element.Tag) -> str:
    """Выбираю ссылку из тэга"""
    return encoded_next_link_tag["href"]


def append_wiki_hostname(pathname_and_query: str) -> str:
    """Добавляю доменное имя"""
    return ORIGINE_AND_HOSTNAME + pathname_and_query


def save_next_link_to_file(filename: str, url: str) -> None:
    """Записываю в файл ссылку на следующую страницу"""
    with open(filename, mode="w") as file:
        file.write(url)


def get_animals_list(soup: BeautifulSoup) -> list:
    """Получаю список животных"""

    page_content = soup.find("div", class_="mw-category mw-category-columns")
    return [link.text for link in page_content.find_all("a")]


def count_animals_per_letter(animals_list: list[str]) -> dict:
    """Получаю словарь,

    где ключи — буквы русского алфавита,
    а значения — то, сколько раз на текущей странице
    встречается животное на эти буквы
    """
    res = {letter: 0 for letter in RUSSIAN_ALPHABET}
    for animal in animals_list:
        try:
            res[animal[0]] += 1

        # На последней странице встречаются латинские буквы, их пропускаем
        except KeyError:
            continue
    return res


def get_previous_count_of_animals(file_to_read: str) -> dict:
    """Считываю, сколько животных было в предыдущие итерации"""
    with open(file_to_read, mode="r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        saved_res = {}
        for row in spamreader:
            # ключи и значения разделены запятой
            # в каждом ряду лежит список
            key, value = row[0].split(",")
            # мне нужно представить значения в виде int, чтобы ниже сложить их с количеством животных в текущей итерации
            saved_res[key] = int(value)
        return saved_res


def save_beasts(
    result_file: str, current_animals_count: dict, previous_animals_count: dict
) -> None:
    """Подсчитываю, сколько всего животных на букву алфавита найдено

    с первого цикла до завершения этой итерации
    и записываю результат в файл
    """
    with open(result_file, mode="w+") as file:
        for key, value in current_animals_count.items():
            try:
                # добавляю количество ранее найденных на эту букву животных
                value += previous_animals_count[key]
                file.write(f"{key},{value}\n")
            except KeyError:
                # если это первая итерация, то файл 'beasts.csv' пустой
                # заполняю его значениями из res
                file.write(f"{key},{value}\n")


def main():
    url = get_link_to_current_page_from_csv(NEXT_LINK_SCV)
    # выбираю див, в котором лежит ссылка на следующую страницу
    soup = get_soup(url)
    page_content = soup.find("div", id="mw-pages")
    encoded_next_link_tag = get_link_to_next_page_from_tag(page_content)
    pathname_and_query = get_pathname_and_query(encoded_next_link_tag)
    next_url = append_wiki_hostname(pathname_and_query)
    decoded_next_url = unquote(next_url)
    save_next_link_to_file(filename=NEXT_LINK_SCV, url=decoded_next_url)
    animals_list = get_animals_list(soup)
    current_animals_count = count_animals_per_letter(animals_list)
    previous_animals_count = get_previous_count_of_animals(RESULT_FILE)
    save_beasts(RESULT_FILE, current_animals_count, previous_animals_count)


if __name__ == "__main__":
    main()
