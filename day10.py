from typing import List, Dict, Tuple, Set

from collections import Counter

import random

def parse_input(file: str) -> List[int]:
    inputs: List[int] = []
    with open(file, 'r') as f:
        for line in f:
            inputs.append(int(line.strip()))
    return inputs


inputs: List[int] = parse_input('data/day10_data')


def is_in_range(base_num: int ,num: int, num_range: Tuple[int, int]) -> bool:
    lo = num_range[0]
    hi = num_range[1]
    if (lo + base_num) <= num <= (hi + base_num):
        return True
    return False


def count_diffs(inputs: List[int],
                adapter_jolt_range: Tuple[int, int],
                built_in_jolts: int = 3,
                outlet_jolt: int = 0) -> int:
    lo: int = adapter_jolt_range[0]
    hi: int = adapter_jolt_range[1]
    diffs: List[int] = []
    inputs_copy = inputs.copy()
    inputs_copy = sorted(inputs_copy)
    current_rating = outlet_jolt
    idx = -1
    while current_rating <= inputs_copy[-1]:
        if (idx + hi) == (len(inputs_copy) - 1):
            last_numbers: List[int] = inputs_copy[idx + 1:]
            numbers_seen: Set[int] = set()
            small_idx = 0
            while len(numbers_seen) < len(last_numbers):
                candidate = last_numbers[small_idx]
                if is_in_range(current_rating, candidate, adapter_jolt_range):
                    next_adapter = candidate
                    diffs.append((abs(next_adapter - current_rating)))
                    current_rating = next_adapter
                    numbers_seen.add(candidate)
                    small_idx += 1
            break
        else:
            candidates: List[Tuple[int, int]] = [(inputs_copy[idx + i], i) for i in range(lo, hi + 1)
                                                 if is_in_range(current_rating, inputs_copy[idx + i], adapter_jolt_range)]
            next_adapter = candidates[0][0]    # always take the lowest
            diffs.append((abs(next_adapter - current_rating)))
            current_rating = next_adapter
            idx += 1

    diffs.append(built_in_jolts)    # always the same
    counts_of_diffs: Dict[int, int] = Counter(diffs)
    return counts_of_diffs[lo] * counts_of_diffs[hi]

# for test0
# assert count_diffs(inputs, (1, 3)) == 35
# for test1
# assert count_diffs(inputs, (1, 3)) == 220

print(count_diffs(inputs, (1, 3)))

# Part 2 #
def is_count_possible(inputs: List[int],
                adapter_jolt_range: Tuple[int, int],
                built_in_jolts: int = 3,
                outlet_jolt: int = 0) -> bool:
    lo: int = adapter_jolt_range[0]
    hi: int = adapter_jolt_range[1]
    diffs: List[int] = []
    inputs_copy = inputs.copy()
    inputs_copy = sorted(inputs_copy)
    built_in_adapter = inputs_copy[-1] + built_in_jolts
    current_rating = outlet_jolt
    idx = -1
    while current_rating <= inputs_copy[-1]:
        if (idx + hi) == (len(inputs_copy) - 1):
            last_numbers: List[int] = inputs_copy[idx + 1:]
            numbers_seen: Set[int] = set()
            small_idx = 0
            while len(numbers_seen) < len(last_numbers):
                candidate = last_numbers[small_idx]
                if is_in_range(current_rating, candidate, adapter_jolt_range):
                    next_adapter = candidate
                    diffs.append((abs(next_adapter - current_rating)))
                    current_rating = next_adapter
                    numbers_seen.add(candidate)
                    small_idx += 1
            break
        else:
            candidates: List[Tuple[int, int]] = [(inputs_copy[idx + i], i) for i in range(lo, hi + 1)
                                                 if is_in_range(current_rating, inputs_copy[idx + i], adapter_jolt_range)]
            next_adapter = candidates[0][0]    # always take the lowest
            diffs.append((abs(next_adapter - current_rating)))
            current_rating = next_adapter
            idx += 1

    if (current_rating + built_in_jolts) == built_in_adapter:
        return True
    else:
        return False

arrangements = 0
idx = 0
#current_rating = 0

"""
Not entirely efficient way...
"""

def check_inputs(inputs: List[int], current_rating: int, adapter_jolt_range: Tuple[int, int] = (1, 3),
                built_in_jolts: int = 3,
                outlet_jolt: int = 0) -> None:
    global arrangements
    global idx
    #global current_rating
    lo = adapter_jolt_range[0]
    hi = adapter_jolt_range[1]
    candidates: List[int] = []
    built_in_adapter = max(inputs) + built_in_jolts
    # base case
    if (current_rating + built_in_jolts) == built_in_adapter:
        arrangements += 1
        return None     # possibly add else and return
    # TODO: Deal with edge cases here.
    for i in range(lo, hi + 1):
        if is_in_range(base_num=current_rating, num=inputs[idx + i], num_range=adapter_jolt_range):
            candidates.append(inputs[idx + i])
    for candidate in candidates:
        # TODO: recurse on each candidate as current_rating
        new_inputs = inputs[:(idx + 1)] + [candidate]
        check_inputs(new_inputs, candidate)

    idx += 1
