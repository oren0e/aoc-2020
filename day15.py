from typing import List, Dict

from collections import defaultdict


def memory_game(starting_numbers: List[int], end_turn: int = 2020) -> int:
    """
    Returns the number spoken at turn 'end_turn'
    """
    spoken_dict: Dict[int, List[int]] = defaultdict(list)   # number: list of turns it was spoken
    spoken_numbers: List[int] = []
    turn = 1
    # read from starting numbers
    for num in starting_numbers:
        spoken_numbers.append(num)
        spoken_dict[num].append(turn)
        turn += 1

    while turn <= end_turn:
        if len(spoken_dict[spoken_numbers[-1]]) == 1:   # first time spoken
            if spoken_numbers[-1] == spoken_numbers[-2] == 0:
                spoken_numbers.append(1)
                spoken_dict[1].append(turn)
            else:
                spoken_numbers.append(0)
                spoken_dict[0].append(turn)
        else:
            diff: int = spoken_dict[spoken_numbers[-1]][-1] - spoken_dict[spoken_numbers[-1]][-2]
            if spoken_numbers[-1] == spoken_numbers[-2] == diff:
                spoken_numbers.append(1)
                spoken_dict[1].append(turn)
            else:
                spoken_numbers.append(diff)
                spoken_dict[diff].append(turn)
        turn += 1
    return spoken_numbers[-1]


assert memory_game([0, 3, 6]) == 436
assert memory_game([1, 3, 2]) == 1
assert memory_game([2, 1, 3]) == 10
assert memory_game([1, 2, 3]) == 27
assert memory_game([2, 3, 1]) == 78
assert memory_game([3, 2, 1]) == 438
assert memory_game([3, 1, 2]) == 1836

INPUT = [8, 13, 1, 0, 18, 9]
print(memory_game(INPUT))


## Part 2 ##
assert memory_game([0, 3, 6], end_turn=30000000) == 175594
assert memory_game([1, 3, 2], end_turn=30000000) == 2578
assert memory_game([2, 1, 3], end_turn=30000000) == 3544142
assert memory_game([1, 2, 3], end_turn=30000000) == 261214
assert memory_game([2, 3, 1], end_turn=30000000) == 6895259
assert memory_game([3, 2, 1], end_turn=30000000) == 18
assert memory_game([3, 1, 2], end_turn=30000000) == 362

print(memory_game(INPUT, end_turn=30000000))
