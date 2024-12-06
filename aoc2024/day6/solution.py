from collections import defaultdict, namedtuple
from itertools import cycle
from typing import Dict, List, Set, Tuple

from aoc2024.helpers import load_data

Point = namedtuple('Point', ['x', 'y'])


def preprocess(data: List[str]) -> List[str]:
    return data


DIRECTIONS = [
    (0, -1),  # Up
    (1, 0),  # Right
    (0, 1),  # Down
    (-1, 0),  # Left
]


def find_guard(lab_map: List[str]) -> Point:
    for i, row in enumerate(lab_map):
        for j, cell in enumerate(row):
            if cell == '^':
                return Point(j, i)


def move_guard(
    lab_map: List[str], start: Point, obstacle: Point | None = None
) -> Dict[Point, Set[Tuple[int, int]]] | None:
    rows = len(lab_map)
    cols = len(lab_map[0])

    cur_x, cur_y = start.x, start.y
    dir_cycle = cycle(DIRECTIONS)
    dx, dy = next(dir_cycle)
    # Dictionary to store visited cells, as well as the direction the guard was moving when it visited them.
    visited = defaultdict(set)

    while 0 <= cur_x + dx < cols and 0 <= cur_y + dy < rows:
        # While within bounds, add current cell and repeat.
        visited[Point(cur_x, cur_y)].add((dx, dy))
        if lab_map[cur_y + dy][cur_x + dx] == '#':
            dx, dy = next(dir_cycle)
            visited[Point(cur_x, cur_y)].add((dx, dy))
        if obstacle is not None and (cur_x + dx, cur_y + dy) == (obstacle.x, obstacle.y):
            dx, dy = next(dir_cycle)
        cur_x += dx
        cur_y += dy
        # Check for loops
        if (dx, dy) in visited.get(Point(cur_x, cur_y), set()):
            return None

    # Don't forget to add the item at the last visited cell.
    visited[Point(cur_x, cur_y)].add((dx, dy))

    return visited


def solve_part1(lab_map: List[str]) -> int:
    start = find_guard(lab_map)
    visited = move_guard(lab_map, start)
    return len(visited)


def solve_part2(lab_map: List[str]) -> int:
    start = find_guard(lab_map)
    candidates = move_guard(lab_map, start)

    return sum(
        [
            1 if move_guard(lab_map, start, obstacle=point) is None else 0
            for point in candidates.keys()
            if point != start
        ]
    )


def solution():
    data = preprocess(load_data(6))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
