from collections import defaultdict
from functools import cmp_to_key
from typing import Dict, List, Set, Tuple

from aoc2024.helpers import load_data


def preprocess(data: str) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    rules, updates = data.split('\n\n')
    rule_map = defaultdict(set)
    for rule in rules.split('\n'):
        rule = rule.split('|')
        rule_map[int(rule[0])].add(int(rule[1]))

    updates = [[int(x) for x in update.split(',')] for update in updates.split('\n')]
    return rule_map, updates


def is_correct_update(rules: Dict[int, Set[int]], update: List[int]) -> bool:
    for idx, val in enumerate(update):
        rule = rules.get(val, [])
        if any(after in update[:idx] for after in rule):
            return False

    return True


def solve_part1(rules: Dict[int, Set[int]], updates: List[List[int]]) -> int:
    result = []
    for update in updates:
        if is_correct_update(rules, update):
            result.append(update)

    return sum([update[len(update) // 2] for update in result])


def fix_update(rules: Dict[int, Set[int]], update: List[int]) -> List[int]:
    def cmp(a: int, b: int):
        """
        Comparator for two items.
        """
        # If b is in the rules of a, a should come first
        if b in rules.get(a, set()):
            return 1
        # If a is in the rules of b, b should come first
        if a in rules.get(b, set()):
            return -1

        # No rules apply
        return 0

    return sorted(update, key=cmp_to_key(cmp))


def solve_part2(rules: Dict[int, List[int]], updates: List[List[int]]) -> int:
    result = []
    for update in updates:
        if not is_correct_update(rules, update):
            result.append(fix_update(rules, update))

    return sum([update[len(update) // 2] for update in result])


def solution():
    data = preprocess(load_data(5, as_single_string=True))
    print("Part 1:")
    print(solve_part1(*data))
    print("Part 2:")
    print(solve_part2(*data))
