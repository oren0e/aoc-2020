from __future__ import annotations

from typing import NamedTuple, List

import re


class Tile(NamedTuple):
    value: int
    image: List[List[str]]

    @staticmethod
    def parse(raw_tile: str) -> Tile:
        raw_splited = raw_tile.split('\n')
        tile_num = int(re.search(r'(\d+)', raw_splited[0]).group(1))
        img = [[c for c in row] for row in raw_splited[1:]]
        return Tile(tile_num, img)


def parse_input(file: str) -> List[Tile]:
    with open(file, 'r') as f:
        raw = f.read()
    return [Tile.parse(t) for t in raw.split('\n\n')]

tiles = parse_input('data/day20_test')