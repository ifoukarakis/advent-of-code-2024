from typing import List, Tuple, Set
from itertools import cycle
from collections import defaultdict

from aoc2024.helpers import load_data


def preprocess(data: List[str]) -> List[str]:
    return data


DIRECTIONS = cycle([
    (0, -1),  # Up
    (1, 0),  # Right
    (0, 1),  # Down
    (-1, 0),  # Left
])


def find_guard(lab_map: List[str]) -> Tuple[int, int]:
    for i, row in enumerate(lab_map):
        for j, cell in enumerate(row):
            if cell == '^':
                return j, i


def move_guard(lab_map: List[str], start_x: int, start_y: int) -> Set[Tuple[int, int]]:
    rows = len(lab_map)
    cols = len(lab_map[0])

    cur_x, cur_y = start_x, start_y
    dx, dy = next(DIRECTIONS)
    visited = defaultdict(set)

    while 0 <= cur_x + dx < cols and 0 <= cur_y + dy < rows:
        # While within bounds, repeat
        visited[(cur_x, cur_y)].add((dx, dy))
        if lab_map[cur_y + dy][cur_x + dx] == '#':
            dx, dy = next(DIRECTIONS)
        cur_x += dx
        cur_y += dy

    # Don't forget to add the item at the last position
    visited[(cur_x, cur_y)].add((dx, dy))

    return visited


def solve_part1(lab_map: List[str]) -> int:
    start_x, start_y = find_guard(lab_map)
    visited = move_guard(lab_map, start_x, start_y)
    return len(visited)


def solve_part2(lab_map: List[str]) -> int:
    pass


def solution():
    data = preprocess(load_data(6))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
