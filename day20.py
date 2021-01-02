from __future__ import annotations

from typing import NamedTuple, List, Dict, Tuple, Optional, Union

from collections import defaultdict

import re

import math

import itertools

from functools import reduce


class Tile(NamedTuple):
    value: int
    image: List[List[str]]

    @staticmethod
    def parse(raw_tile: str) -> Tile:
        raw_splited = raw_tile.split('\n')
        tile_num = int(re.search(r'(\d+)', raw_splited[0]).group(1))
        img = [[c for c in row] for row in raw_splited[1:]]
        return Tile(tile_num, img)

    def extract_edges(self) -> Dict[str, List[str]]:
        """
        Returns list of North, South, East and West edges
        """
        edges: Dict[str, List[str]] = {}
        edges['N'] = self.image[0]
        edges['S'] = self.image[-1]
        edges['E'] = [row[-1] for row in self.image]
        edges['W'] = [row[0] for row in self.image]
        return edges

    def flip(self, axis: str = "h") -> Tile:
        """
        Return a new image flipped around axis.
        'h' for horizontal, 'v' for vertical, 'o' for original (no flip)
        """
        img = self.image.copy()
        if axis == "h":    # South becomes North etc.
           img = [row for row in reversed(img)]
        elif axis == "v":
            img = [list("".join(row)[::-1]) for row in img]
        elif axis == 'o':
            pass
        else:
            raise ValueError(f"Invalid orientation {axis}")
        return Tile(value=self.value, image=img)

    @staticmethod
    def _rotate_90(img: List[List[str]]) -> List[List[str]]:
        return list(zip(*reversed(img)))

    def rotate(self, degrees: int) -> Tile:
        """
        Rotate clockwise by `degress` (90, 180, 270)
        """
        img = self.image.copy()
        if degrees == 90:
            img = self._rotate_90(img)
        elif degrees == 180:
            img = self._rotate_90(self._rotate_90(img))
        elif degrees == 270:
            img = self._rotate_90(self._rotate_90(self._rotate_90(img)))
        else:
            raise ValueError(f"degrees should be one of (90, 180, 270). Not {degrees}")
        return Tile(value=self.value, image=img)

    def print_image(self) -> None:
        for row in self.image:
            print("".join(row))

def parse_input(file: str) -> List[Tile]:
    with open(file, 'r') as f:
        raw = f.read()
    return [Tile.parse(t) for t in raw.split('\n\n')]

tiles = parse_input('data/day20_test')


def compare_edges(tile1_edges: Dict[str, List[str]], tile2_edges: Dict[str, List[str]]) ->\
        Dict[str, int]:
    """
    Returns the count of identical edges
    """
    res_dict = defaultdict(int)     # for which edge in tile1 it has identical edges with tile2
    if tile1_edges['N'] == tile2_edges['S']:
        res_dict['N'] += 1
    elif tile1_edges['S'] == tile2_edges['N']:
        res_dict['S'] += 1

    elif tile1_edges['E'] == tile2_edges['W']:
        res_dict['E'] += 1
    elif tile1_edges['W'] == tile2_edges['E']:
        res_dict['W'] += 1
    return res_dict


def count_matching_edges_of_pair(tile1: Tile, tile2: Tile) ->\
        Dict[Tuple[Union[str, int], ...], Tuple[int, Optional[str]]]:
    """
    Try all combinations of possible states of a tile:
    h for horizontal axis flip, v for vertical axis flip,
    and o for original.
    """
    res_dict: Dict[Tuple[Union[str, int], ...], Tuple[int, Optional[str]]] = {}
    for combo in itertools.product(['h', 'v', 'o', 90, 180, 270], ['h', 'v', 'o', 90, 180, 270]):
        if isinstance(combo[0], str):
            cand1: Tile = tile1.flip(combo[0])
        elif isinstance(combo[0], int):
            cand1: Tile = tile1.rotate(combo[0])
        else:
            raise ValueError(f"Unknown transformation {combo[0]}")

        if isinstance(combo[1], str):
            cand2: Tile = tile2.flip(combo[1])
        elif isinstance(combo[1], int):
            cand2: Tile = tile2.rotate(combo[1])
        else:
            raise ValueError(f"Unknown transformation {combo[1]}")


        cand1_edges = cand1.extract_edges()
        cand2_edges = cand2.extract_edges()
        comp_dict = compare_edges(cand1_edges, cand2_edges)
        sum_identical: int = sum(v for v in comp_dict.values())
        if sum_identical > 0:
            res_dict[combo] = (sum_identical,
                               [key for key, value in comp_dict.items() if value > 0][0])   # might be a problem here if
                                                                                            # pair of tiles can have more
                                                                                            # than 1 identical edge for a given
                                                                                            # transformation
        else:
            res_dict[combo] = (sum_identical, None)
    return res_dict

# a = count_matching_edges_of_pair(tiles[0], tiles[1])


def count_matching_edges(the_tile: Tile, tiles: List[Tile]) -> \
        Dict[Tuple[int, int], Tuple[int, Dict[Tuple[Union[str, int], ...], Tuple[int, str]]]]:
    """
    Returns dict in the form of:
    {(tile1.value, tile2.value): (num_nonzero_edges,
     {(flip_axis_to_tile1, flip_axis_to_tile2): (num_identical_edges, edge_type)})}
    """
    res_dict: Dict[Tuple[int, int], Tuple[int, Dict[Tuple[Union[str, int], ...], Tuple[int, str]]]] = {}
    for tile in tiles:
        res_dict[(the_tile.value, tile.value)] = \
            (sum(v[0] for v in count_matching_edges_of_pair(the_tile, tile).values()),
             count_matching_edges_of_pair(the_tile, tile))
    return res_dict


def get_tiles_minus(tile: Tile, tiles: List[Tile]) -> List[Tile]:
    return [t for t in tiles if t.value != tile.value]


# a = count_matching_edges(tiles[1], get_tiles_minus(tiles[1], tiles))

def count_non_zero_edges(pairs_dict: Dict[Tuple[int, int], Tuple[int, Dict[Tuple[Union[str, int], ...], Tuple[int, str]]]])\
        -> int:
    return sum(v[0] > 0 for v in pairs_dict.values())

"""
For part 1 we can just find the corner tiles by checking
non zero edges == 2
"""
def get_corner_tiles(tiles: List[Tile]) -> List[int]:
    res_list: List[int] = []
    for tile in tiles:
        pairs_dict = count_matching_edges(tile, get_tiles_minus(tile, tiles))
        if count_non_zero_edges(pairs_dict) == 2:
            res_list.append(tile.value)
    return res_list


# test
# assert reduce(lambda x,y: x*y, get_corner_tiles(tiles)) == 20899048083289

# print(reduce(lambda x, y: x*y, get_corner_tiles(tiles)))



# TODO:
#   1. Think how to put the tiles in place
#   One direction is put a corner one and then continue to the next that fits next to it
#   if it fits, continue, if not go back one step and try another one from the options
#
#
#
#

def rearange_tiles(tiles: List[Tile]) -> List[Tile]:
    """
    Corner tiles need 2 other tiles with common edges
    Edge tile need 3
    All other need 4
    """
    num_in_row = math.sqrt(len(tiles))  # since its a square arrangement
    res_list: List[Optional[Tile]] = [None for _ in range(len(tiles))]
    for i, tile in enumerate(tiles):
        pairs_dict = count_matching_edges(tile, get_tiles_minus(tile, tiles))
        non_zero_tiles = count_non_zero_edges(pairs_dict)