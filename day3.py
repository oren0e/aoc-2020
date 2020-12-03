from typing import NamedTuple, Dict, List

from math import ceil

class Slope(NamedTuple):
    up: int
    down: int
    right: int
    left: int


slope = Slope(up=0, down=1, right=3, left=0)


class Coordinate(NamedTuple):
    x: int
    y: int


"""
We want to take the number of lines in our input (length) and multiply it by 3
(the ratio of the slope) and that is our desired width

Function to do that:
1. count all the lines (=len)
2. for each line
    duplicate it (concat to itself) (len*3 // line_length) - 1 times
    write it to file
"""


def build_map(read_file_path: str, write_file_path: str) -> None:
    with open(read_file_path, 'r') as f:
        # get dimensions
        for num_lines, line in enumerate(f):
            line1: str = line.strip()
            if num_lines == 0:
                line_length = len(line1)
        num_lines += 1
        ratio = (slope.right // slope.down)
        mult_times = ((num_lines * ratio) // line_length) + 1

    f = open(read_file_path, 'r')
    f_map = open(write_file_path, 'w')
    for line in f:
        line1: str = line.strip()
        mult_line = line1 * mult_times + '\n'
        f_map.write(mult_line)
    f.close()
    f_map.close()

# build_map('data/day3_example', 'data/day3_map')
build_map('data/day3_data', 'data/day3_map')


def parse_map(map_file: str) -> Dict[Coordinate, bool]:
    locations: Dict[Coordinate, bool] = {}  # tree = True, no tree = False
    with open(map_file, 'r') as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                if c == '#':
                    locations[Coordinate(i, j)] = True
                else:
                    locations[Coordinate(i, j)] = False
    return locations


def count_trees(map_file: str) -> int:
    locations: Dict[Coordinate, bool] = parse_map(map_file)
    num_trees: int = 0
    loc_x = 0
    loc_y = 0
    position = Coordinate(loc_x, loc_y)
    while position in locations:
        if locations[position]:
            num_trees += 1
        loc_y += slope.right      # right = add 3
        loc_x += slope.down      # down = add 1
        position = Coordinate(loc_x, loc_y)
    return num_trees


# for test case
#assert count_trees('data/day3_map') == 7
print(count_trees('data/day3_map'))

# Part 2 #
def check_slope(slope: Slope, read_file_path: str, map_file: str) -> int:
    def build_map() -> None:
        with open(read_file_path, 'r') as f:
            # get dimensions
            for num_lines, line in enumerate(f):
                line1: str = line.strip()
                if num_lines == 0:
                    line_length = len(line1)
            num_lines += 1
            ratio = ceil(slope.right / slope.down)
            mult_times = ((num_lines * ratio) // line_length) + 1

        f = open(read_file_path, 'r')
        f_map = open(map_file, 'w')
        for line in f:
            line1: str = line.strip()
            mult_line = line1 * mult_times + '\n'
            f_map.write(mult_line)
        f.close()
        f_map.close()

    def parse_map() -> Dict[Coordinate, bool]:
        locations: Dict[Coordinate, bool] = {}  # tree = True, no tree = False
        with open(map_file, 'r') as f:
            for i, line in enumerate(f):
                for j, c in enumerate(line.strip()):
                    if c == '#':
                        locations[Coordinate(i, j)] = True
                    else:
                        locations[Coordinate(i, j)] = False
        return locations

    def count_trees() -> int:
        locations: Dict[Coordinate, bool] = parse_map()
        num_trees: int = 0
        loc_x = 0
        loc_y = 0
        position = Coordinate(loc_x, loc_y)
        while position in locations:
            if locations[position]:
                num_trees += 1
            loc_y += slope.right  # right = add 3
            loc_x += slope.down  # down = add 1
            position = Coordinate(loc_x, loc_y)
        return num_trees

    build_map()
    return count_trees()


assert check_slope(Slope(0, 1, 3, 0), 'data/day3_example', 'data/day3_map') == 7
print(check_slope(Slope(0, 1, 3, 0), 'data/day3_data', 'data/day3_map'))


# Part 2 #

slopes: List[Slope] = [Slope(0, 1, 1, 0),
                       Slope(0, 1, 3, 0),
                       Slope(0, 1, 5, 0),
                       Slope(0, 1, 7, 0),
                       Slope(0, 2, 1, 0)]

def mult_slopes(read_path: str, map_file_path: str) -> int:
    res: int = 1
    for s in slopes:
        res *= check_slope(s, read_path, map_file_path)
    return res

# assert mult_slopes('data/day3_example', 'data/day3_map') == 336
print(mult_slopes('data/day3_data', 'data/day3_map'))