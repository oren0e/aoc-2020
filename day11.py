from typing import List, Tuple

from copy import deepcopy

Layout = List[List[str]]

def parse_input(file: str) -> Layout:
    res_list: List[List[str]] = []
    with open(file, 'r') as f:
        for line in f:
            res_list.append([c for c in line.strip()])
    return res_list

orig_layout: Layout = parse_input('data/day11_test')
day11_layout: Layout = parse_input('data/day11_data')
part2_test0_layout: Layout = parse_input('data/day11_part2_test0')
part2_test1_layout: Layout = parse_input('data/day11_part2_test1')


def n(i: int, j: int, layout: Layout) -> bool:
    """
    Returns True if the North adjacent seat is taken,
    False otherwise.
    """
    try:
        if (i - 1) >= 0:
            if layout[i - 1][j] == "#":
                return True
            return False
        return False
    except IndexError:
        return False


def s(i: int, j: int, layout: Layout) -> bool:
    try:
        if layout[i + 1][j] == "#":
            return True
        return False
    except IndexError:
        return False


def e(i: int, j: int, layout: Layout) -> bool:
    try:
        if layout[i][j + 1] == "#":
            return True
        return False
    except IndexError:
        return False


def w(i: int, j: int, layout: Layout) -> bool:
    try:
        if (j - 1) >= 0:
            if layout[i][j - 1] == "#":
                return True
            return False
        return False
    except IndexError:
        return False


def nw(i: int, j: int, layout: Layout) -> bool:
    try:
        if ((i - 1) >= 0) and ((j - 1) >= 0):
            if layout[i - 1][j - 1] == "#":
                return True
            return False
        return False
    except IndexError:
        return False


def se(i: int, j: int, layout: Layout) -> bool:
    try:
        if layout[i + 1][j + 1] == "#":
            return True
        return False
    except IndexError:
        return False


def ne(i: int, j: int, layout: Layout) -> bool:
    try:
        if (i - 1) >= 0:
            if layout[i - 1][j + 1] == "#":
                return True
            return False
        return False
    except IndexError:
        return False


def sw(i: int, j: int, layout: Layout) -> bool:
    try:
        if (j - 1) >= 0:
            if layout[i + 1][j - 1] == "#":
                return True
            return False
        return False
    except IndexError:
        return False


def run_round(layout: Layout) -> Tuple[Layout, bool]:
    # i for rows ,j for columns
    #res_layout: Layout = [["L" for seat in row] for row in layout]
    changed: bool = False
    res_layout = deepcopy(layout)
    for i, sub_lst in enumerate(layout):
        for j, seat in enumerate(sub_lst):
            if (seat == 'L') and ((s(i, j, layout) + n(i, j, layout) + w(i, j, layout) +
                                   e(i, j, layout) + nw(i, j, layout) + ne(i, j, layout) + sw(i, j, layout) + se(i, j, layout)) == 0):
                res_layout[i][j] = "#"
                changed = True
            elif (seat == '#') and ((s(i, j, layout) + n(i, j, layout) + w(i, j, layout) +
                                   e(i, j, layout) + nw(i, j, layout) + ne(i, j, layout) + sw(i, j, layout) + se(i, j, layout)) >= 4):
                res_layout[i][j] = "L"
                changed = True
    return res_layout, changed


def count_occupied(orig_layout: Layout) -> int:
    l, _ = run_round(orig_layout)
    while True:
        l, flag = run_round(l)
        if not flag:
            break
    return sum(seat == "#" for sub_list in l for seat in sub_list)


#assert count_occupied(orig_layout) == 37
#print(count_occupied(day11_layout))

## Part 2 ##
def n2(i: int, j: int, layout: Layout) -> bool:
        """
        Returns True if the first Northen seat is taken,
        False otherwise.
        """
        try:
            sub = 1
            if (i - 1) >= 0:
                if layout[i - 1][j] == "#":
                    return True
                elif layout[i - 1][j] == ".":
                    while layout[i - sub][j] == ".":
                        sub += 1
                        if (i - sub) >= 0:
                            if layout[i - sub][j] == "#":
                                return True
                        else:
                            return False
                    return False
                else:
                    return False
            return False
        except IndexError:
            return False


def s2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if layout[i + 1][j] == "#":
            return True
        elif layout[i + 1][j] == ".":
            while layout[i + sub][j] == ".":
                sub += 1
                if layout[i + sub][j] == "#":
                    return True
            return False
        else:
            return False
    except IndexError:
        return False


def e2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if layout[i][j + 1] == "#":
            return True
        elif layout[i][j + 1] == ".":
            while layout[i][j + sub] == ".":
                sub += 1
                if layout[i][j + sub] == "#":
                    return True
            return False
        else:
            return False
    except IndexError:
        return False

def w2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if (j - 1) >= 0:
            if layout[i][j - 1] == "#":
                return True
            elif layout[i][j - 1] == ".":
                while layout[i][j - sub] == ".":
                    sub += 1
                    if (j - sub) >= 0:
                        if layout[i][j - sub] == "#":
                            return True
                    else:
                        return False
                return False
            else:
                return False
        return False
    except IndexError:
        return False


def nw2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if ((j - 1) >= 0) and ((i - 1) >= 0):
            if layout[i - 1][j - 1] == "#":
                return True
            elif layout[i - 1][j - 1] == ".":
                while layout[i - sub][j - sub] == ".":
                    sub += 1
                    if ((j - sub) >= 0) and ((i - sub) >= 0):
                        if layout[i - sub][j - sub] == "#":
                            return True
                    else:
                        return False
                return False
            else:
                return False
        return False
    except IndexError:
        return False


def se2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if layout[i + 1][j + 1] == "#":
            return True
        elif layout[i + 1][j + 1] == ".":
            while layout[i + sub][j + sub] == ".":
                sub += 1
                if layout[i + sub][j + sub] == "#":
                    return True
            return False
        else:
            return False
    except IndexError:
        return False


def ne2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if (i - 1) >= 0:
            if layout[i - 1][j + 1] == "#":
                return True
            elif layout[i - 1][j + 1] == ".":
                while layout[i - sub][j + sub] == ".":
                    sub += 1
                    if (i - sub) >= 0:
                        if layout[i - sub][j + sub] == "#":
                            return True
                    else:
                        return False
                return False
            else:
                return False
        return False
    except IndexError:
        return False


def sw2(i: int, j: int, layout: Layout) -> bool:
    try:
        sub = 1
        if (j - 1) >= 0:
            if layout[i + 1][j - 1] == "#":
                return True
            elif layout[i + 1][j - 1] == ".":
                while layout[i + sub][j - sub] == ".":
                    sub += 1
                    if (j - sub) >= 0:
                        if layout[i + sub][j - sub] == "#":
                            return True
                    else:
                        return False
                return False
            else:
                return False
        return False
    except IndexError:
        return False


def run_round2(layout: Layout) -> Tuple[Layout, bool]:
    # i for rows ,j for columns
    changed: bool = False
    res_layout = deepcopy(layout)
    for i, sub_lst in enumerate(layout):
        for j, seat in enumerate(sub_lst):
            if (seat == 'L') and ((s2(i, j, layout) + n2(i, j, layout) + w2(i, j, layout) +
                                   e2(i, j, layout) + nw2(i, j, layout) + ne2(i, j, layout) + sw2(i, j, layout) + se2(i, j, layout)) == 0):
                res_layout[i][j] = "#"
                changed = True
            elif (seat == '#') and ((s2(i, j, layout) + n2(i, j, layout) + w2(i, j, layout) +
                                   e2(i, j, layout) + nw2(i, j, layout) + ne2(i, j, layout) + sw2(i, j, layout) + se2(i, j, layout)) >= 5):
                res_layout[i][j] = "L"
                changed = True
    return res_layout, changed


def count_occupied2(orig_layout: Layout) -> int:
    l, _ = run_round2(orig_layout)
    while True:
        l, flag = run_round2(l)
        if not flag:
            break
    return sum(seat == "#" for sub_list in l for seat in sub_list)

#count_occupied2(part2_test0_layout)
#count_occupied2(part2_test1_layout)
assert count_occupied2(orig_layout) == 26
print(count_occupied2(day11_layout))