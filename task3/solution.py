def break_interval_into_seconds(start: int, stop: int) -> set:
    return {
        second for second in range(start, stop + 1)
    }  # !important it has to be +1 otherwise you miss the last second, see range() docs


def make_timeline(intervals: list[int]) -> set:
    res_timeline = set()

    # every odd element is interval END, every previous element is interval START
    for i in range(1, len(intervals), 2):
        interval_timeline = break_interval_into_seconds(intervals[i - 1], intervals[i])
        res_timeline = res_timeline | interval_timeline
    return res_timeline


def calculate_attendance(
    lesson_intervals: list[int], pupil_intervals: list[int], tutor_intervals: list[int]
) -> int:
    lesson_timeline = make_timeline(lesson_intervals)
    pupil_timeline = make_timeline(pupil_intervals)
    tutor_timeline = make_timeline(tutor_intervals)

    seconds_when_tutor_meet_pupil = lesson_timeline & pupil_timeline & tutor_timeline
    return len(seconds_when_tutor_meet_pupil)
