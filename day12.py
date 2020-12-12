from typing import List, Dict, NamedTuple, Tuple

class Instruction(NamedTuple):
    kind: str
    value: int


def parse_input(file: str) -> List[Instruction]:
    res_lst: List[Instruction] = []
    with open(file, 'r') as f:
        for line in f:
            res_lst.append(Instruction(kind=line.strip()[0], value=int(line.strip()[1:])))
    return res_lst


instructions_test: List[Instruction] = parse_input('data/day12_test')
instructions_day12: List[Instruction] = parse_input('data/day12_data')


class Navigator:
    def __init__(self, start: str = 'E') -> None:
        self.start = start
        self.x: int = 0     # controls East/West
        self.y: int = 0     # controls North/South
        self.current_direction: str = start
        self.directions: List[str] = ['N', 'E', 'S', 'W']

    def determine_direction_from(self, direction: str, degrees: int) -> str:
        if direction == 'R':
            idx = (self.directions.index(self.current_direction) + (degrees // 90)) % len(self.directions)
        elif direction == 'L':
            idx = (self.directions.index(self.current_direction) - (degrees // 90)) % len(self.directions)
        else:
            raise ValueError(f"Invalid direction {direction}")
        return self.directions[idx]

    def move_forward(self, value: int) -> None:
        if self.current_direction == 'N':
            self.y += value
        elif self.current_direction == 'S':
            self.y -= value
        elif self.current_direction == 'E':
            self.x += value
        elif self.current_direction == 'W':
            self.x -= value
        else:
            raise ValueError(f"Invalid current direction {self.current_direction}")

    def navigate(self, instructions: List[Instruction]) -> Tuple[int, int]:
        for instruction in instructions:
            if (instruction.kind == 'R') or (instruction.kind == 'L'):
                self.current_direction = self.determine_direction_from(instruction.kind, instruction.value)
            elif instruction.kind == 'F':
                self.move_forward(instruction.value)
            elif instruction.kind == 'N':
                self.y += instruction.value
            elif instruction.kind == 'S':
                self.y -= instruction.value
            elif instruction.kind == 'E':
                self.x += instruction.value
            elif instruction.kind == 'W':
                self.x -= instruction.value
        return self.x, self.y

    @staticmethod
    def manhattan_dist(x: int, y: int, start_x: int = 0, start_y: int = 0) -> int:
        return abs(start_x - x) + abs(start_y - y)

    def get_endpoint_manhattan(self, instructions: List[Instruction]) -> int:
        x, y = self.navigate(instructions)
        return self.manhattan_dist(x, y)

# nv = Navigator()
# assert nv.get_endpoint_manhattan(instructions_test) == 25

# nv = Navigator()
# print(nv.get_endpoint_manhattan(instructions_day12))


## Part 2 ##
class Navigator2:
    def __init__(self, start: str = 'NE') -> None:
        self.start = start
        self.x: int = 0     # controls East/West
        self.y: int = 0     # controls North/South
        self.waypoint_x: int = 10
        self.waypoint_y: int = 1
        self.current_direction: str = start     # current waypoint direction
        self.directions: List[str] = ['NE', 'SE', 'SW', 'NW']
        self.directions_coords: Dict[str, Tuple[int, int]] = {
            'NE': (1, 1),
            'SE': (1, -1),
            'SW': (-1, -1),
            'NW': (-1, 1)
        }

    def determine_waypoint_direction_from(self, direction: str, degrees: int) -> None:
        if direction == 'R':
            idx = (self.directions.index(self.current_direction) + (degrees // 90)) % len(self.directions)
        elif direction == 'L':
            idx = ((self.directions.index(self.current_direction) - (degrees // 90)) % len(self.directions))
            degrees = -degrees + 360
        else:
            raise ValueError(f"Invalid direction {direction}")

        if degrees == 90:
            self.waypoint_x, self.waypoint_y = self.waypoint_y, (-1) * self.waypoint_x
        elif degrees == 180:
            self.waypoint_x, self.waypoint_y = (-1) * self.waypoint_x, (-1) * self.waypoint_y
        elif degrees == 270:
            self.waypoint_x, self.waypoint_y = (-1) * self.waypoint_y, self.waypoint_x
        self.current_direction = self.directions[idx]

    def move_forward(self, value: int) -> None:
        self.x += self.waypoint_x * value
        self.y += self.waypoint_y * value

    def navigate(self, instructions: List[Instruction]) -> Tuple[int, int]:
        for instruction in instructions:
            if (instruction.kind == 'R') or (instruction.kind == 'L'):
                self.determine_waypoint_direction_from(instruction.kind, instruction.value)
            elif instruction.kind == 'F':
                self.move_forward(instruction.value)
            elif instruction.kind == 'N':
                self.waypoint_y += instruction.value
            elif instruction.kind == 'S':
                self.waypoint_y -= instruction.value
            elif instruction.kind == 'E':
                self.waypoint_x += instruction.value
            elif instruction.kind == 'W':
                self.waypoint_x -= instruction.value
        return self.x, self.y

    @staticmethod
    def manhattan_dist(x: int, y: int, start_x: int = 0, start_y: int = 0) -> int:
        return abs(start_x - x) + abs(start_y - y)

    def get_endpoint_manhattan(self, instructions: List[Instruction]) -> int:
        x, y = self.navigate(instructions)
        return self.manhattan_dist(x, y)


nv = Navigator2()
assert nv.get_endpoint_manhattan(instructions_test) == 286

nv2 = Navigator2()
print(nv2.get_endpoint_manhattan(instructions_day12))
