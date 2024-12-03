from pathlib import Path
from typing import List

import duckdb

DATA_DIR = Path(__file__).parent.parent / 'data'


def load_data(day: int, as_single_string: bool = False) -> List[str] | str:
    """
    Load the data for a given day. Assumes the data is in a file called input.txt in a folder called data/day{day}
    :param day: the day to load the data for.
    :param as_single_string: if True, return the data as a single string, otherwise return a list of strings,
                             one for each line in the input file.
    :return: a list of strings, one for each line in the input file.
    """
    with open(DATA_DIR / f'day{day}' / 'input.txt') as f:
        if as_single_string:
            return f.read()
        return f.read().splitlines()


def load_data_to_duckdb(day: int, as_single_string: bool = False):
    """
    Load the data for a given day into a duckdb table. Assumes the data is in a file called input.txt in a folder
    called data/day{day}. Table will be named raw_day_<day number> and has a single column, named 'line'.
    :param day: the day to load the data for.
    :param as_single_string: if True, load to a new table with a single row containing the entire file as a single
     string.
    """
    if as_single_string:
        duckdb.sql(
            f"""
            CREATE TABLE raw_day_{day} AS
                FROM read_blob('data/day{day}/input.txt')
            """
        )
    else:
        duckdb.sql(
            f"""
            CREATE TABLE raw_day_{day} AS
                FROM read_csv('data/day{day}/input.txt', header=false, columns={{'line': 'VARCHAR'}})
            """
        )
