from typing import Set, List

from collections import Counter


def count_yes(file: str) -> int:
    yes_count = 0
    group_set: Set[str] = set()
    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                yes_count += len(group_set)
                group_set = set()
                continue
            else:
                group_set = group_set.union(set(line.strip()))
    yes_count += len(group_set)     # last case treatment
    return yes_count


# assert count_yes('data/day6_test') == 11
print(count_yes('data/day6_data'))


# Part 2 #
def count_yes2(file: str) -> int:
    yes_count = 0
    group_list: List[str] = []
    group_count = 0
    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                value_counts = Counter(group_list)
                yes_count += sum(1 for v in value_counts.values() if v == group_count)
                group_count = 0
                group_list = []
            else:
                group_list += list(set(line.strip()))
                group_count += 1
    value_counts = Counter(group_list)
    yes_count += sum(1 for v in value_counts.values() if v == group_count)
    return yes_count


# assert count_yes2('data/day6_test') == 6
print(count_yes2('data/day6_data'))