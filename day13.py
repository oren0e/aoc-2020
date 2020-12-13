from typing import List, Tuple

from math import ceil

from functools import reduce


def parse_input(file: str) -> Tuple[int, List[int]]:
    """
    Treat 'x' as -1
    """
    with open(file, 'r') as f:
        raw = f.read()
    raw = raw.split('\n')
    earliest: int = int(raw[0])
    bus_list: List[int] = [int(num) if num != 'x' else -1 for num in raw[1].split(',')]
    return earliest, bus_list


def find_earliest_bus(my_time: int, bus_list: List[int]) -> Tuple[int, float]:
    min_diff = float('inf')
    min_id = 0
    for bus_id in bus_list:
        if bus_id == -1:
            continue
        res = ceil(my_time / bus_id) * bus_id
        diff = res - my_time
        if diff < min_diff:
            min_diff = diff
            min_id = bus_id
    return min_id, min_diff


def mult_wait_time_bus_id(bus_id: int, min_diff: float) -> float:
    return min_diff * bus_id


def ans_part1(file: str) -> float:
    mytime, bus_list = parse_input(file)
    min_id, min_diff = find_earliest_bus(mytime, bus_list)
    return mult_wait_time_bus_id(min_id, min_diff)

#assert ans_part1('data/day13_test') == 295
#print(ans_part1('data/day13_data'))


## Part 2 ##
def find_timestamp(bus_list: List[int], start: int = 0) -> int:
    buses: List[Tuple[int, int]] = [(i, bus_id) for i, bus_id in enumerate(bus_list) if bus_id != -1]
    x = start

    def check_timestamp(ts: int, bus_ind: int, bus_id: int) -> bool:
        return True if (((ts + bus_ind) % bus_id) == 0) else False

    while True:
        if all(check_timestamp(x, *bus) for bus in buses):
            return x
        else:
            x += 1


#assert find_timestamp(parse_input('data/day13_test')[1]) == 1068781

#assert find_timestamp([17,-1,13,19]) == 3417
#assert find_timestamp([67,7,59,61]) == 754018.
#assert find_timestamp([67,-1,7,59,61]) == 779210.
#assert find_timestamp([67,7,-1,59,61]) == 1261476.
#assert find_timestamp([1789,37,47,1889]) == 1202161486.


def get_remainders(bus_list: List[int]) -> List[Tuple[int, int]]:
    buses: List[Tuple[int, int]] = [(i, bus_id) for i, bus_id in enumerate(bus_list) if bus_id != -1]
    remainders = [(bus_id, (bus_id - ind) % bus_id) for ind, bus_id in buses]
    return remainders


"""
Brute force won't work here. This problem relies on knowing about Chineese Remainder Theorem. Not cool!
Code for this taken from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6 
"""


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


get_remainders(parse_input('data/day13_data')[1])
n, a = zip(*get_remainders(parse_input('data/day13_data')[1]))
print(chinese_remainder(n, a))
