from typing import List, Union


def parse_input(file) -> List[List[Union[int, str]]]:
    with open(file, 'r') as f:
        res: List[List[Union[int, str]]] = []
        for line in f:
            parts: List[str] = line.strip().split()
            nums: List[int] = [int(num) for num in parts[0].split('-')]
            lett: str = [item[0] for item in parts[1]][0]
            res.append(nums + [lett] + [parts[2]])

    return res

# data: List[List[Union[int, str]]] = parse_input('day2_part1_test')
data: List[List[Union[int, str]]] = parse_input('day2_part1_data')


def check_input(inp: List[Union[str, int]]) -> bool:
    num_times = inp[3].count(inp[2])
    if (num_times >= inp[0]) and (num_times <= inp[1]):
        return True
    return False


# assert sum(check_input(i) for i in data) == 2
print(sum(check_input(i) for i in data))

# Part 2 #

# data: List[List[Union[int, str]]] = parse_input('day2_part1_test')


def check_input2(inp: List[Union[str, int]]) -> bool:
    pos1: str = inp[3][inp[0] - 1]
    pos2: str = inp[3][inp[1] - 1]
    if ((pos1 == inp[2]) or (pos2 == inp[2])) and (not ((pos1 == inp[2]) and (pos2 == inp[2]))):
        return True
    return False


# assert sum(check_input2(i) for i in data) == 1
print(sum(check_input2(i) for i in data))
