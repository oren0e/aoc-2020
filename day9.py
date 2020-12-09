from typing import List, NamedTuple, Dict, Tuple, Optional


def parse_input(file: str) -> List[int]:
    inputs: List[int] = []
    with open(file, 'r') as f:
        for line in f:
            inputs.append(int(line.strip()))
    return inputs

inputs: List[int] = parse_input('data/day9_data')


def find_sum_range(lst: List[int]) -> Tuple[int, int]:
    lst_copy = lst.copy()
    lst_copy = sorted(lst_copy)
    lo = lst_copy[0] + lst_copy[1]
    hi = lst_copy[-2] + lst_copy[-1]
    return lo, hi


def is_valid(num: int, inputs: List[int]) -> bool:
    lo, hi = find_sum_range(inputs)
    if lo <= num <= hi:
        return True
    return False


def find_anomaly_number(inputs: List[int], preamble_size: int = 25) -> Optional[int]:
    left_idx = 0
    right_idx = preamble_size
    while right_idx < len(inputs):
        current_lst: List[int] = inputs[left_idx: right_idx]
        num_to_check = inputs[right_idx]
        if not is_valid(num_to_check, current_lst):
            return num_to_check
        left_idx += 1
        right_idx += 1
    print("All numbers were valid")
    return None

# test
# assert find_anomaly_number(inputs, 5) == 127
#find_anomaly_number(inputs)

# Part 2 #
"""
Brute force way, probably there is a better solution
"""
def find_summands(target: int, inputs: List[int]) -> List[int]:
    idx = 0
    summands: List[int] = []
    while idx < len(inputs):
        for i in range(idx, len(inputs)):
            summands.append(inputs[i])
            if sum(summands) > target:
                break
            if sum(summands) == target:
                return summands
        summands = []
        idx += 1

# for test
# target_num: int = find_anomaly_number(inputs, 5)
# ans_lst: List[int] = find_summands(target_num, inputs)
# assert min(ans_lst) + max(ans_lst) == 62

target_num: int = find_anomaly_number(inputs)
ans_lst: List[int] = find_summands(target_num, inputs)
print(min(ans_lst) + max(ans_lst))