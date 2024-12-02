from typing import List, Tuple

from aoc2024.helpers import load_data


def preprocess(data: List[str]) -> Tuple[List[int]]:
    return [list(map(int, x.split())) for x in data]


def is_safe(values: List[int]) -> bool:
    """
    Check if a report is safe.
    :param values: the values for a specific level.
    :return: whether the report is unsafe.
    """
    if values == sorted(values) or values == sorted(values, reverse=True):
        return all(0 < abs(values[i] - values[i + 1]) <= 3 for i in range(len(values) - 1))

    return False


def solve_part1(values: Tuple[List[int]]) -> int:
    return sum([is_safe(val) for val in values])


def solve_part2(values: Tuple[List[int]]) -> int:

    def is_safe_with_dampener(values: List[int]) -> List[int]:
        if is_safe(values):
            return True

        # Check by removing one item each time
        return any(is_safe(values[:i] + values[i + 1 :]) for i in range(len(values)))

    return sum([is_safe_with_dampener(val) for val in values])


def solution():
    data = preprocess(load_data(2))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
