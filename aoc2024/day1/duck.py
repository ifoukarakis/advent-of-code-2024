import duckdb

from aoc2024.helpers import load_data_to_duckdb


def preprocess():
    duckdb.sql(
        """
    CREATE TABLE day1 AS
        SELECT
            CAST(SPLIT_PART(line, '  ', 1) AS INTEGER) AS a,
            CAST(SPLIT_PART(line, '  ', 2) AS INTEGER) AS b
        FROM raw_day_1
    """
    )


def solve_part1() -> int:
    return duckdb.sql(
        """
        WITH a_sorted AS (
            SELECT a, ROW_NUMBER() OVER (ORDER BY a) AS rn
            FROM day1
        ), b_sorted AS (
            SELECT b, ROW_NUMBER() OVER (ORDER BY b) AS rn
            FROM day1
        )
        SELECT SUM(ABS(a - b)) FROM a_sorted JOIN b_sorted ON a_sorted.rn = b_sorted.rn
    """
    ).fetchone()[0]


def solve_part2() -> int:
    return duckdb.sql(
        """
        WITH b_counts AS (
            SELECT b, COUNT(*) AS count
            FROM day1
            GROUP BY b
        )
        SELECT SUM(a * count) FROM day1 JOIN b_counts ON day1.a = b_counts.b
    """
    ).fetchone()[0]


def solution():
    load_data_to_duckdb(1)
    preprocess()
    print("Part 1:")
    print(solve_part1())
    print("Part 2:")
    print(solve_part2())


if __name__ == '__main__':
    solution()
