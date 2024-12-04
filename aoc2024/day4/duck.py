import duckdb

from aoc2024.helpers import load_data_to_duckdb


def preprocess():
    duckdb.sql(
        """
    create table day4 as
        with lines as (
            select
                string_split(decode(content), '\n') as rows,
                unnest(rows) as line,
                generate_subscripts(rows, 1) as row
            from raw_day_4
        )
        select
            string_split(line, '') as cols,
            unnest(cols) as value,
            row,
            generate_subscripts(cols, 1) as col
        from lines
    """
    )


def solve_part1() -> int:
    return duckdb.sql(
        """
            with x as (
                select
                    row, col
                from day4
                where value = 'X'
            ), m as (
               select
                    row, col
                from day4
                where value = 'M'
            ), a as (
               select
                    row, col
                from day4
                where value = 'A'
            ), s as (
               select
                    row, col
                from day4
                where value = 'S'
            )
            select
                m.col - x.col as m_x_dir,
                m.row - x.row as m_y_dir,
                a.col - m.col as a_x_dir,
                a.row - m.row as a_y_dir,
                s.col - a.col as s_x_dir,
                s.row - a.row as s_y_dir
            from
                x
                -- Join X with all neighbouring M
                join m on abs(x.row - m.row) <= 1 and abs(x.col - m.col) <= 1
                -- Join M with all neighbouring A
                join a on abs(m.row - a.row) <= 1 and abs(m.col - a.col) <= 1
                -- Join A with all neighbouring S
                join s on abs(a.row - s.row) <= 1 and abs(a.col - s.col) <= 1
            where
                m_x_dir = a_x_dir and a_x_dir = s_x_dir
                and m_y_dir = a_y_dir and a_y_dir = s_y_dir
        """
    )


def solve_part2() -> int:
    return duckdb.sql(
        """
        with a as (
            select row, col from day4 where value = 'A'
        ), mas as (
            select row, col, value from day4 where value in ('M', 'S')
        )
       select
            a.row,
            a.col,
            ul.value || dr.value as diag1,
            dl.value || ur.value as diag2
        from
            a
            -- Join with full to get elements of diagonals
            -- Up-Left
            join mas ul on ul.row = a.row - 1 and ul.col = a.col - 1
            -- Up-Right
            join mas ur on ur.row = a.row - 1 and ur.col = a.col + 1
            -- Down-Left
            join mas dl on dl.row = a.row + 1 and dl.col = a.col - 1
            -- Down-Right
            join mas dr on dr.row = a.row + 1 and dr.col = a.col + 1
        where
            diag1 in ('MS', 'SM') and diag2 in ('MS', 'SM')
        """
    )


def solution():
    load_data_to_duckdb(4, as_single_string=True)
    preprocess()
    print("Part 1:")
    print(solve_part1())
    print("Part 2:")
    print(solve_part2())


if __name__ == '__main__':
    solution()
