from typing import NamedTuple, List, Tuple, Dict, Union


class Instruction:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value
        self.been_executed: bool = False
        self.checked: bool = False

    def __repr__(self) -> str:
        return repr(f"Instruction(name: {self.name}, value: {self.value}, been_executed: {self.been_executed}, "
                    f"checked: {self.checked})")

def parse_input(file: str) -> List[Instruction]:
    instructions: List[Instruction] = []
    with open(file, 'r') as f:
        for line in f:
            stripped = line.strip().split()
            instructions.append(Instruction(stripped[0], int(stripped[1])))
    return instructions


instructions: List[Instruction] = parse_input('data/day8_data')


def value_before_second(instructions: List[Instruction]) -> int:
    counter = 0
    ptr = 0
    while True:
        if (instructions[ptr].name == 'nop') and (not instructions[ptr].been_executed):
            instructions[ptr].been_executed = True
            ptr += 1
        elif (instructions[ptr].name == 'acc') and (not instructions[ptr].been_executed):
            instructions[ptr].been_executed = True
            counter += instructions[ptr].value
            ptr += 1
        elif (instructions[ptr].name == 'jmp') and (not instructions[ptr].been_executed):
            instructions[ptr].been_executed = True
            ptr += instructions[ptr].value
        else:
            #print(ptr)  # 350 + 1 = 351
            break
    return counter

#value_before_second(instructions)

# Part 2 #
def run_program(instructions: List[Instruction]) -> Union[bool, int]:
    """
    Returns False if loop is present, else will come to IndexError probably
    and will return counter
    """
    counter = 0
    ptr = 0
    while True:
        try:
            if (instructions[ptr].name == 'nop') and (not instructions[ptr].been_executed):
                instructions[ptr].been_executed = True
                ptr += 1
            elif (instructions[ptr].name == 'acc') and (not instructions[ptr].been_executed):
                instructions[ptr].been_executed = True
                counter += instructions[ptr].value
                ptr += 1
            elif (instructions[ptr].name == 'jmp') and (not instructions[ptr].been_executed):
                instructions[ptr].been_executed = True
                ptr += instructions[ptr].value
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return counter


def reset_instructions(instructions: List[Instruction]) -> None:
    for instruction in instructions:
        instruction.been_executed = False


def find_fix(instructions: List[Instruction]) -> int:
    """
    Returns the position for the instruction to change
    """
    for ptr, instruction in enumerate(instructions):
        if instruction.name == 'jmp':
            instruction.name = 'nop'
            res: Union[bool, int] = run_program(instructions)
            if res:
                print(res)
                return ptr
            else:
                instruction.name = 'jmp'
                instruction.checked = True
        elif instruction.name == 'nop':
            instruction.name = 'jmp'
            res: Union[bool, int] = run_program(instructions)
            if res:
                print(res)
                return ptr
            else:
                instruction.name = 'nop'
                instruction.checked = True
        reset_instructions(instructions)

find_fix(instructions)