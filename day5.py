from typing import List

"""
BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
"""


def partition(inputs: List[str], upper_ind: str, lower_ind: str, start: int) -> int:
    upper = start - 1
    lower = 0
    for letter in inputs:
        rng = upper - lower
        if letter == lower_ind:
            upper -= (rng // 2) + 1
        elif letter == upper_ind:
            lower += (rng // 2) + 1
        else:
            raise ValueError("Unknown indicator")
    assert lower == upper, "lower is not equal to upper!"
    return upper


def decode_bpass(bpass: str) -> int:
    """
    Returns seat ID
    """
    rows_data: List[str] = list(bpass[:-3])
    cols_data: List[str] = list(bpass[-3:])
    row = partition(rows_data, 'B', 'F', 128)
    col = partition(cols_data, 'R', 'L', 8)
    return (row * 8) + col


assert decode_bpass('FBFBBFFRLR') == 357
assert decode_bpass('BFFFBBFRRR') == 567
assert decode_bpass('FFFBBBFRRR') == 119
assert decode_bpass('FFFBBBFRRR') == 119
assert decode_bpass('BBFFBBFRLL') == 820

with open('data/day5_data', 'r') as f:
    INPUTS: List[str] = [line.strip() for line in f]

print(max(decode_bpass(bpass) for bpass in INPUTS))


# Part 2 #
def find_my_seat(inputs: List[str]) -> int:
    seat_ids: List[int] = [decode_bpass(bpass) for bpass in inputs]
    sorted_ids = sorted(seat_ids)
    lo = sorted_ids[0]
    hi = sorted_ids[-1]
    for i, seat in enumerate(sorted_ids, start=lo):
        if i != seat:
            return i


print(find_my_seat(INPUTS))

