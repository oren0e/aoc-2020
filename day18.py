from typing import List

import re

RAW1 = "1 + 2 * 3 + 4 * 5 + 6"


def one_calculation(expression: str) -> int:
    """
    expression is a string in the form of
    'a op b'
    """
    split_exp = expression.split()
    if split_exp[1] == "+":
        return int(split_exp[0]) + int(split_exp[-1])
    elif split_exp[1] == "*":
        return int(split_exp[0]) * int(split_exp[-1])


def calculate_simple_line(line: str) -> int:
    first_expression = re.match(r'(^\d+\s.\s\d+)', line).group(1)
    rest_of_expression = re.split(f"{re.escape(first_expression)}", line)
    if all(c == "" for c in rest_of_expression):
        return one_calculation(first_expression)
    else:
        current = one_calculation(first_expression)
        line = line.replace(first_expression, str(current), 1)
        return calculate_simple_line(line)


assert calculate_simple_line(RAW1) == 71
assert calculate_simple_line("5 + 6") == 11
assert calculate_simple_line("2 * 3") == 6
assert calculate_simple_line("4 * 11") == 44
assert calculate_simple_line("44 * 10") == 440
assert calculate_simple_line("1 + 4 + 44") == 49
assert calculate_simple_line("44 * 55 * 10") == 24200

RAW2 = "1 + (2 * 3) + (4 * (5 + 6))"


def calculate_full_line(line: str) -> int:
    expression = list(line)
    s: List[int] = []
    while (")" in line) or ("(" in line):
        for i, c in enumerate(line):
            if c == "(":
                s: List[int] = []
                s.append(i)
            elif c == ")" and s:
                start_ind = s.pop()
                expression[start_ind:(i + 1)] = str(calculate_simple_line(line[(start_ind + 1):i]))
                break
        line = "".join(expression)
    return calculate_simple_line(line)


assert calculate_full_line(RAW2) == 51
assert calculate_full_line("2 * 3 + (4 * 5)") == 26
assert calculate_full_line("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert calculate_full_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert calculate_full_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

assert calculate_full_line("9 + 5 * 6 + 7 * 9 + 5") == 824


def get_sum_of_lines(file: str) -> int:
    with open(file, 'r') as f:
        return sum(calculate_full_line(line.strip()) for line in f)

# print(get_sum_of_lines('data/day18_data'))


## Part 2 ##
def calc_addition(orig_addition: str) -> str:
    addition = re.sub(r"\+", lambda ele: " " + ele[0] + " ", orig_addition)

    if addition.count("+") == 1:
        current = one_calculation(addition)
        return addition.replace(addition, str(current), 1)
    else:
        first_expression = re.match(r'(^\d+\s.\s\d+)', addition).group(1)

        current = one_calculation(first_expression)
        addition = addition.replace(first_expression, str(current), 1)
        addition = addition.replace(" ", "")
        return calc_addition(addition)


def calculate_simple_line2(line: str) -> int:
    additions: List[str] = re.findall(r'(\d+[\+\d]+)', line.replace(" ", ""))
    if additions:
        for addition in additions:
            if "+" in addition:
                rep = calc_addition(addition)
                spaced_addition = re.sub(r"\+", lambda ele: " " + ele[0] + " ", addition)
                line = line.replace(spaced_addition, rep, 1)

    if re.match(r'(^\d+\s.\s\d+)', line) is None:
        return int(line)
    first_expression = re.match(r'(^\d+\s.\s\d+)', line).group(1)
    rest_of_expression = re.split(f"{re.escape(first_expression)}", line)
    if all(c == "" for c in rest_of_expression):
        return one_calculation(first_expression)
    else:
        current = one_calculation(first_expression)
        line = line.replace(first_expression, str(current), 1)
        return calculate_simple_line2(line)


def calculate_full_line2(line: str) -> int:
    expression = list(line)
    s: List[int] = []
    while (")" in line) or ("(" in line):
        for i, c in enumerate(line):
            if c == "(":
                s: List[int] = []
                s.append(i)
            elif c == ")" and s:
                start_ind = s.pop()
                expression[start_ind:(i + 1)] = str(calculate_simple_line2(line[(start_ind + 1):i]))
                break
        line = "".join(expression)
    return calculate_simple_line2(line)


assert calculate_full_line2("1 + 2 * 3 + 4 * 5 + 6") == 231
assert calculate_full_line2("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert calculate_full_line2("2 * 3 + (4 * 5)") == 46
assert calculate_full_line2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert calculate_full_line2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert calculate_full_line2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


def get_sum_of_lines2(file: str) -> int:
    with open(file, 'r') as f:
        return sum(calculate_full_line2(line.strip()) for line in f)


print(get_sum_of_lines2('data/day18_data'))
