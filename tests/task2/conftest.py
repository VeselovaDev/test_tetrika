import os

import pytest

START_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
NEXT_URL = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom=Азиатские+токи#mw-pages"

ANIMALS = [
    "Чернопопик",
    "Подкустовный выползень",
    "Перепончатокрылый серпень",
    "Хорёк-паникёр",
]

TEST_FILE = "tests/new_file"


@pytest.fixture(scope="function")
def tear_down():
    yield
    os.remove(TEST_FILE)
