from typing import List, Tuple

from aoc2024.helpers import load_data

WORD = 'XMAS'


def preprocess(data: List[str]) -> List[str]:
    return data


def has_match(data: List[str], x: int, y: int, direction: Tuple[int, int]) -> bool:
    rows = len(data)
    cols = len(data[0])
    cur_x, cur_y = x, y
    dx, dy = direction
    current = []
    for _ in range(len(WORD)):
        if cur_x < 0 or cur_y < 0 or cur_x >= cols or cur_y >= rows:
            return False
        current.append(data[cur_x][cur_y])
        cur_x += dx
        cur_y += dy

    return ''.join(current) == WORD


def solve_part1(data: str) -> int:
    rows = len(data)
    cols = len(data[0])
    directions = [
        (1, 0),  # Right
        (-1, 0),  # Left
        (0, 1),  # Down
        (0, -1),  # Up
        (1, -1),  # Up-Right
        (-1, -1),  # Up-Left
        (1, 1),  # Down-Right
        (-1, 1),  # Down-Left
    ]

    positions = []
    for x in range(cols):
        for y in range(rows):
            if data[x][y] == WORD[0]:
                for direction in directions:
                    if has_match(data, x, y, direction):
                        positions.append((x, y))

    return len(positions)


def is_xmas(data: List[str], row: int, col: int) -> bool:
    if data[row][col] != 'A':
        return False

    diagonals = [data[row - 1][col - 1] + data[row + 1][col + 1], data[row - 1][col + 1] + data[row + 1][col - 1]]
    return all(diagonal in {'MS', 'SM'} for diagonal in diagonals)


def solve_part2(data: str) -> int:
    rows = len(data)
    cols = len(data[0])

    positions = []
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if is_xmas(data, col, row):
                positions.append((col, row))
    return len(positions)


def solution():
    data = preprocess(load_data(4))
    print("Part 1:")
    print(solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))
