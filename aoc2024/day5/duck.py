import duckdb

from aoc2024.helpers import load_data_to_duckdb


def preprocess():
    duckdb.sql(
        """
    create table rules as
        with lines as (
          select
            unnest(
                string_split(
                    split_part(decode(content), '\n\n', 1),
                    '\n'
                )
            ) as rule
            from raw_day_5
        )
        select
            split_part(rule, '|', 1)::int as before,
            split_part(rule, '|', 2)::int as after
        from lines
    """
    )

    duckdb.sql(
        """
    create table updates as
        with lines as (
          select
          string_split(
                    split_part(decode(content), '\n\n', 2),
                    '\n'
            ) as lines,
            unnest(lines) as updates,
            generate_subscripts(lines, 1) as update_id
            from raw_day_5
        )
        select
            update_id,
            string_split(updates, ',')::int[] as raw_update,
            unnest(raw_update)::int as page,
            generate_subscripts(raw_update, 1) as index,
            index = (len(raw_update) + 1) // 2 as is_middle
        from lines
    """
    )


def solve_part1() -> int:
    return duckdb.sql(
        """
        with update_validity_check as (
            -- For each update, check if it is a violation by comparing each page with all other pages
            select
                a.update_id,
                a.page as current_page,
                a.index as current_index,
                b.page as downstream_page,
                b.index as downstream_index,
                r.before is not null as is_violation,
                sum(case when is_violation then 1 else 0 end) over (partition by a.update_id) = 0 as valid_update
            from
                updates a
                join updates b on a.update_id = b.update_id
                left join rules r on a.page = r.after and b.page = r.before
            where
                a.index < b.index
            order by a.update_id, current_index, downstream_index
        )
        select
            sum(page)
        from
            updates a
        where
            update_id in (select update_id from update_validity_check where valid_update)
            and is_middle
        """
    )


def solve_part2() -> int:
    pass


def solution():
    load_data_to_duckdb(5, as_single_string=True)
    preprocess()
    print("Part 1:")
    print(solve_part1())
    print("Part 2:")
    print(solve_part2())


if __name__ == '__main__':
    solution()
