# flake8: noqa
import re
from typing import List, Tuple

from aoc2024.helpers import load_data


def preprocess(data: str) -> Tuple[List[int]]:
    return data


def solve_part1(value: str) -> int:
    total = 0
    matches = re.findall(r'mul\(\d{1,3},\d{1,3}\)', value)
    pairs = [x[4:-1].split(',') for x in matches]
    total += sum([int(x) * int(y) for x, y in pairs])
    return total


def solve_part2(value: str) -> int:
    total = 0
    matches = re.findall(r'(do\(\)|don\'t\(\)|mul\(\d{1,3},\d{1,3}\))', value)
    previous = True
    mask = [previous := False if x == "don't()" else True if x == "do()" else previous for x in matches]
    actual_matches = [m for m, do_use in zip(matches, mask) if do_use and m.startswith("mul")]
    pairs = [x[4:-1].split(',') for x in actual_matches]
    total += sum([int(x) * int(y) for x, y in pairs])
    return total


def solution():
    data = preprocess(load_data(3, as_single_string=True))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
