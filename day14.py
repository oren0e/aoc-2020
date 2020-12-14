from typing import List, Tuple, Dict, NamedTuple, Optional

import re

from itertools import product


class Instruction(NamedTuple):
    ptr: int
    value: int


class ProgramUnit(NamedTuple):
    mask: str
    instructions: List[Instruction]


Program = List[ProgramUnit]


def parse_input(file: str) -> Program:
    with open(file, 'r') as f:
        raw = f.read()
    prog_list: List[ProgramUnit] = []
    raw_list = raw.split('mask = ')
    for block in raw_list[1:]:
        block_list = block.strip().split('\n')
        pu = ProgramUnit(block_list[0], [])
        for item in block_list[1:]:
            ptr = re.match(r'.*\[(\d+)\] = (\d+)', item).group(1)
            value = re.match(r'.*\[(\d+)\] = (\d+)', item).group(2)
            pu.instructions.append(Instruction(int(ptr), int(value)))
        prog_list.append(pu)
    return prog_list


test_program: Program = parse_input('data/day14_test')
day14_program: Program = parse_input('data/day14_data')

"""
Because the program is initialized with 0s, it is enough to insert
only the changes to the dictionary and then sum them all.
"""
mem: Dict[int, int] = {}


def apply_binary_mask(mask: str, num: int) -> int:
    """
    Returns decimal number of a 36-bit binary string representation
    of `num` after `mask` application.
    """
    binary_num = f"{num:036b}"
    indices_to_change = [i for i, bit in enumerate(mask) if bit != 'X']
    return int("".join([bit if i not in indices_to_change else mask[i] for i, bit in enumerate(binary_num)]), 2)


def run_program(program: Program) -> int:
    for pu in program:
        mask = pu.mask
        for instruction in pu.instructions:
            mem[instruction.ptr] = apply_binary_mask(mask, instruction.value)
    return sum(value for value in mem.values())


# assert run_program(test_program) == 165
print(run_program(day14_program))


## Part 2 ##
test1_program: Program = parse_input('data/day14_test1')


mem: Dict[int, int] = {}


def get_binary_rule(mask: str, num: int) -> str:
    """
    Returns decimal number of a 36-bit binary string representation
    of `num` after `mask` application.
    """
    binary_num = f"{num:036b}"
    res: List[Optional[str]] = [None for _ in range(len(binary_num))]
    indices_to_change = [i for i, bit in enumerate(mask) if bit != '0']
    for i, bit_num in enumerate(binary_num):
        if i not in indices_to_change:
            res[i] = bit_num
        elif mask[i] == '1':
            res[i] = '1'
        elif mask[i] == 'X':
            res[i] = 'X'
        else:
            raise ValueError(f"Something went wrong at mask {mask}, index {i}")
    return "".join(res)


def get_memory_indices_to_write(bin_rule: str) -> List[int]:
    """
    1. Find all indices that can be changed
    2. For each pairing of (index, combination[j])
       replace with combination[j] at index
    3. Convert to int and append result
    """
    res: List[int] = []
    if 'X' not in bin_rule:
        return [int(bin_rule, 2)]
    indices_to_change = [i for i, char in enumerate(bin_rule) if char == 'X']
    for combination in product('01', repeat=len(indices_to_change)):
        bin_seq: List[str] = list(bin_rule)
        for i, c in zip(indices_to_change, combination):
            bin_seq[i] = c
        res.append(int("".join(bin_seq), 2))
    return res


assert get_memory_indices_to_write('000000000000000000000000000000X1101X') == [26, 27, 58, 59]
assert get_memory_indices_to_write('00000000000000000000000000000001X0XX') == [16, 17, 18, 19, 24, 25, 26, 27]


def run_program_v2(program: Program) -> int:
    for pu in program:
        mask = pu.mask
        for instruction in pu.instructions:
            mem_lst: List[int] = get_memory_indices_to_write(get_binary_rule(mask, instruction.ptr))
            for address in mem_lst:
                mem[address] = instruction.value
    return sum(value for value in mem.values())


# assert run_program_v2(test1_program) == 208
print(run_program_v2(day14_program))
