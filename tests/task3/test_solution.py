from task3.solution import (
    break_interval_into_seconds,
    calculate_attendance,
    make_timeline,
)

# I changed test cases results from the task, see line 4 in solution.py

TEST_CASES = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3121,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3580,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3567,
    },
]


def test_process_interval():
    res = break_interval_into_seconds(1, 3)
    assert res == {1, 2, 3}


def test_make_timeline():
    res = make_timeline([1, 2, 4, 5])
    assert res == {1, 2, 4, 5}


def test_calculate_attendance():
    lesson_duration = [1, 10]
    pupil_attendance = [0, 2, 8, 11]
    tutor_attendance = [1, 5, 9, 10]
    res = calculate_attendance(lesson_duration, pupil_attendance, tutor_attendance)
    assert res == 4


def test_corrected_test_cases():
    for i, test in enumerate(TEST_CASES):
        res = calculate_attendance(
            test["intervals"]["lesson"],
            test["intervals"]["pupil"],
            test["intervals"]["tutor"],
        )
        assert res == test["answer"], (
            f"Error on test case {i}, got {res}, expected {test['answer']}"
        )
