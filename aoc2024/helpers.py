from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).parent.parent / 'data'


def load_data(day: int) -> List[str]:
    """
    Load the data for a given day. Assumes the data is in a file called input.txt in a folder called data/day{day}
    :param day: the day to load the data for.
    :return: a list of strings, one for each line in the input file.
    """
    with open(DATA_DIR / f'day{day}' / 'input.txt') as f:
        return f.read().splitlines()
