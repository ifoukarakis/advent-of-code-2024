import duckdb

from aoc2024.helpers import load_data_to_duckdb


def preprocess():
    duckdb.sql(
        """
    CREATE TABLE day3 AS
        SELECT content FROM raw_day_3
    """
    )


def solve_part1() -> int:
    return duckdb.sql(
        r"""
        with matches as (
            select
                regexp_extract_all(content::varchar, 'mul\(\d{1,3},\d{1,3}\)') as matches,
                unnest(matches) as match,
                generate_subscripts(matches, 1) as index
            from day3
        )
        select
            sum(
                split_part(match[5:len(match)-1], ',', 1)::int
                * split_part(match[5:len(match)-1], ',', 2)::int
            ) as result
        from matches
        """
    )


def solve_part2() -> int:
    return duckdb.sql(
        r"""
        with matches as (
            select
                regexp_extract_all(decode(content), $$(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))$$) as matches,
                unnest(matches) as match,
                generate_subscripts(matches, 1) as index,
                match in ('do()', 'don''t()') as is_instruction
            from day3
        ), instructions as (
            select
                index,
                match
            from matches where is_instruction
        ), matches_with_previous_instruction as (
            select
                m.match,
                m.index,
                m.is_instruction,
                i.index as instruction_index,
                coalesce(i.match, 'do()') as previous_instruction
            from
                matches m
                left join instructions i on m.index > i.index
            qualify row_number() over(partition by m.index order by i.index desc) = 1
        )
            select
                sum(
                    split_part(match[5:len(match)-1], ',', 1)::int
                    * split_part(match[5:len(match)-1], ',', 2)::int
                ) as result
            from matches_with_previous_instruction
            where
                not is_instruction
                and previous_instruction = 'do()'
        """
    )


def solution():
    load_data_to_duckdb(3, as_single_string=True)
    preprocess()
    print("Part 1:")
    print(solve_part1())
    print("Part 2:")
    print(solve_part2())


if __name__ == '__main__':
    solution()
