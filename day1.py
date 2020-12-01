from typing import List, Dict, Tuple

from collections import defaultdict

data: Dict[int, List[int]] = defaultdict(list)

expense_report: List[int] = [1721,
979,
366,
299,
675,
1456]

with open('day1_data', 'r') as f:
    for line in f:
        val = int(line.strip())
        data[val].append(val)

# for item in expense_report:
#     data[item].append(item)


def find_sum(target: int) -> Tuple[int, int]:
    for key in data.keys():
        lookup_key = target - key
        if data.get(lookup_key) is not None:
            return key, lookup_key

# a, b = find_sum(2020)
# assert a * b == 514579
# print(a*b)

# Part 2
def find_sum3(target: int) -> Tuple[int, int, int]:
    for key in data.keys():
        for key2 in data.keys():
            lookup_key = target - key - key2
            if data.get(lookup_key) is not None:
                return key, key2, lookup_key

a, b, c = find_sum3(2020)
# assert a * b * c == 241861950
print(a * b * c)