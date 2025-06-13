import pytest

from task1.solution import strict


def test_case_1_from_task():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    res = sum_two(1, 2)
    assert res == 3


def test_case_2_from_task():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    with pytest.raises(TypeError):
        sum_two(1, 2.4)


def test_function_without_annotated_return():
    @strict
    def sum_two(a: int, b: int):
        return a + b

    res = sum_two(1, 2)
    assert res == 3


def test_case_args_and_kwargs():
    @strict
    def sum_numbers(a: int, b: int, c: int, d: int) -> int:
        return a + b + c + d

    res = sum_numbers(1, 2, c=3, d=4)
    assert res == 10


def test_case_argument_not_annotated():
    @strict
    def sum_two(a, b: int) -> int:
        return a + b

    with pytest.raises(TypeError):
        sum_two(1, 2)


def test_decorator_works_with_all_required_types():
    @strict
    def common_everybody(a: bool, b: bool, c: int, d: float, e: str) -> tuple:
        return a, b, c, d, e

    res = common_everybody(True, False, 15, 12.3, "kek")
    assert res == (True, False, 15, 12.3, "kek")


def test_kwarg_order_different_from_signature():
    @strict
    def common_everybody(a: bool, b: bool, c: int, d: float, e: str) -> tuple:
        return a, b, c, d, e

    res = common_everybody(b=False, a=True, d=12.3, c=15, e="kek")
    assert res == (True, False, 15, 12.3, "kek")


def test_wrong_type_of_kwarg():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    with pytest.raises(TypeError):
        sum_two(a=5, b="lol")


def test_function_has_no_arguments():
    @strict
    def boring_function() -> int:
        return "It just works"

    assert boring_function() == "It just works"
