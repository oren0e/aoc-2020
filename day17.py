from __future__ import annotations

from typing import NamedTuple, Set, Iterator

import itertools


"""
This problem was a little bit hard for me (was hard to understand) thus I got help from other solutions.
The idea in the coordinates is starting at 0 (top of grid slice) and increasing 
when going down. E.g y = 1 will mark the second row, etc.

Grid will hold the active points.
"""

class Point(NamedTuple):
    x: int
    y: int
    z: int

    def get_neighbors(self) -> Iterator[Point]:
        for dx, dy, dz in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            if (dx != 0) or (dy != 0) or (dz != 0):
                yield Point(self.x + dx, self.y + dy, self.z + dz)


Grid = Set[Point]


def make_grid(file: str) -> Grid:
    with open(file, 'r') as f:
        raw = f.read()
    raw_split = raw.split('\n')
    return {Point(x, y, 0) for y, row in enumerate(raw_split)
                   for x, col in enumerate(row)
                   if col == "#"}


grid_test = make_grid('data/day17_test')
grid_day17 = make_grid('data/day17_data')

def run(grid: Grid) -> Grid:
    possibilities = {p for point in grid for p in point.get_neighbors() if p not in grid}
    new_grid = set()

    for point in grid:
        n = sum(p in grid for p in point.get_neighbors())   # how many neighbors are active
        if n in (2, 3):
            new_grid.add(point)

    for point in possibilities:
        n = sum(p in grid for p in point.get_neighbors())   # how many neighbors are active
        if n == 3:
            new_grid.add(point)
    return new_grid

# test
# for _ in range(6):
#   grid_test = run(grid_test)

# assert len(grid_test) == 112

# for _ in range(6):
#     grid_day17 = run(grid_day17)
# print(len(grid_day17))


## Part 2 ##
class Point2(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def get_neighbors(self) -> Iterator[Point2]:
        for dx, dy, dz, dw in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            if (dx != 0) or (dy != 0) or (dz != 0) or (dw != 0):
                yield Point2(self.x + dx, self.y + dy, self.z + dz, self.w + dw)


Grid2 = Set[Point2]


def make_grid2(file: str) -> Grid2:
    with open(file, 'r') as f:
        raw = f.read()
    raw_split = raw.split('\n')
    return {Point2(x, y, 0, 0) for y, row in enumerate(raw_split)
                   for x, col in enumerate(row)
                   if col == "#"}


grid2_test = make_grid2('data/day17_test')
grid2_day17 = make_grid2('data/day17_data')

def run2(grid: Grid2) -> Grid2:
    possibilities = {p for point in grid for p in point.get_neighbors() if p not in grid}
    new_grid = set()

    for point in grid:
        n = sum(p in grid for p in point.get_neighbors())   # how many neighbors are active
        if n in (2, 3):
            new_grid.add(point)

    for point in possibilities:
        n = sum(p in grid for p in point.get_neighbors())   # how many neighbors are active
        if n == 3:
            new_grid.add(point)
    return new_grid

# test
# for _ in range(6):
#   grid2_test = run2(grid2_test)
#
# assert len(grid2_test) == 848

for _ in range(6):
    grid2_day17 = run(grid2_day17)
print(len(grid2_day17))
