from collections import Counter
from typing import List, Tuple

from aoc2024.helpers import load_data


def preprocess(data: List[str]) -> Tuple[List[int]]:
    list_a = []
    list_b = []
    for line in data:
        a, b = line.split()
        list_a.append(int(a))
        list_b.append(int(b))

    return list_a, list_b


def solve_part1(values: Tuple[List[int]]) -> int:
    a, b = values
    return sum([abs(x - y) for x, y in zip(sorted(a), sorted(b))])


def solve_part2(values: Tuple[List[int]]) -> int:
    a, b = values
    counts = Counter(b)
    return sum([x * counts[x] for x in a])


def solution():
    data = preprocess(load_data(1))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
