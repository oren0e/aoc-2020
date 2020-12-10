from typing import List, Dict, Tuple, Set

from collections import Counter


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
