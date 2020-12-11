from typing import List, Dict, Tuple, Set

from collections import Counter


def parse_input(file: str) -> List[int]:
    inputs: List[int] = []
    with open(file, 'r') as f:
        for line in f:
            inputs.append(int(line.strip()))
    return inputs


inputs: List[int] = parse_input('data/day10_test0')
inputs1: List[int] = parse_input('data/day10_test1')
inputs_day10: List[int] = parse_input('data/day10_data')

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

# print(count_diffs(inputs, (1, 3)))

# Part 2 #
"""
Totally different approach
"""

def count_ways(inputs: List[int]) -> int:
    inputs.append(0)
    inputs.append(max(inputs) + 3)
    last_adapter = inputs[-1]

    # res_array[i] is number of ways to get to i
    res_array: List[int] = [0] * (last_adapter + 1)

    res_array[0] = 1
    if 1 in inputs:
        res_array[1] = 1
    if (2 in inputs) and (1 in inputs):
        res_array[2] = 2
    elif 2 in inputs:
        res_array[2] = 1

    """
    Because of the max +3 gap between the adapters, there must be some adapter that is in inputs
    for i to satisfy i - 1 to i - 3.
    """
    for i in range(3, last_adapter + 1):
        if i not in inputs:
            continue
        res_array[i] = res_array[i - 1] + res_array[i - 2] + res_array[i - 3]

    return res_array[last_adapter]

# test 0
assert count_ways(inputs) == 8
assert count_ways(inputs1) == 19208
print(count_ways(inputs_day10))