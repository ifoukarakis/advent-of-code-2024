import duckdb

from aoc2024.helpers import load_data_to_duckdb


def preprocess():
    duckdb.sql(
        """
    CREATE TABLE day2 AS
        SELECT
            row_number() OVER () AS record_id,
            string_split(line, ' ') AS record,
            unnest(record) AS x,
            unnest(record)::int AS x_int,
            generate_subscripts(record, 1) as index
        FROM raw_day_2
    """
    )


def solve_part1() -> int:
    return duckdb.sql(
        """
        with sorted_records as (
            select
                record_id,
                record,
                array_agg(x order by x_int) as sorted_asc,
                array_agg(x order by x_int desc) as sorted_desc
            from day2
            group by record_id, record
        ), level_diffs as (
            select
                *,
                abs(x_int - lag(x_int) over (partition by record_id order by index)) as diff
            from day2
        ), level_diffs_agg as (
            select
                record_id,
                count_if(diff = 0 or diff > 3) as count_outside_bounds
            from level_diffs
            group by record_id
        )
        select
            count(distinct sr.record_id) as valid_records
        from
            sorted_records sr
            join level_diffs_agg ld on sr.record_id = ld.record_id
        where
            (sr.record = sr.sorted_asc or sr.record = sr.sorted_desc)
            and ld.count_outside_bounds = 0
    """
    )


def solve_part2() -> int:
    return duckdb.sql(
        """
    with sublists as (
        -- Create all possible sublists using cross join magic
        select
            t1.record_id || '-' || t1.index as sublist_id,
            t2.record_id as record_id,
            t2.x_int as x,
            -- Not needed, but was useful for debugging
            t2.index as previous_index,
            -- Let's create a new index for the sublist. It might be ok to use index, but helps keep things clearer
            row_number() over (partition by sublist_id order by t2.index) as sublist_index
        from day2 t1 cross join day2 t2
        where
            t1.record_id = t2.record_id and t1.index <> t2.index
    ), all_lists as (
        -- The dataset to consider is the union of the original list and the sublists
        select * from sublists

        union

        select
            record_id || '-orig' as sublist_id,
            record_id,
            x_int as x,
            index as previous_index,
            index as sublist_index
        from day2
    ),
    -- Pretty much the same logic as part 1, but now we need to group or partition by sublist_id as well
    sorted_records as (
        select
            sublist_id,
            record_id,
            array_agg(x order by sublist_index) as sublist_record,
            array_agg(x order by x) as sorted_asc,
            array_agg(x order by x desc) as sorted_desc
        from all_lists
        group by 1, 2
    ), level_diffs as (
        select
            *,
            abs(x - lag(x) over (partition by sublist_id, record_id order by sublist_index)) as diff
        from all_lists
    ), level_diffs_agg as (
        select
            sublist_id,
            record_id,
            count_if(diff = 0 or diff > 3) as count_outside_bounds
        from level_diffs
        group by sublist_id, record_id
    )
    select
        count(distinct sr.record_id) as valid_records
    from
        sorted_records sr
        join level_diffs_agg ld on sr.record_id = ld.record_id and sr.sublist_id = ld.sublist_id
    where
        (sr.sublist_record = sr.sorted_asc or sr.sublist_record = sr.sorted_desc)
        and ld.count_outside_bounds = 0
      """
    )


def solution():
    load_data_to_duckdb(2)
    preprocess()
    print("Part 1:")
    print(solve_part1())
    print("Part 2:")
    print(solve_part2())


if __name__ == '__main__':
    solution()
