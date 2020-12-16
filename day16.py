from typing import List, Dict, Tuple, Set

from collections import defaultdict

import re

from functools import reduce


def parse_input(file: str) -> Tuple[Dict[str, List[Tuple[int, int]]], List[int], List[List[int]]]:
    req: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    nearby_tickets: List[List[int]] = []

    with open(file, 'r') as f:
        raw = f.read()
    raw_lst = raw.split('\n\n')

    # requirements (fields)
    for requirement in raw_lst[0].strip().split('\n'):
        field_name, rng1, rng2 = re.findall(r'(.*): (\d+-\d+) or (\d+-\d+)', requirement)[0]
        rng1 = tuple(int(num) for num in rng1.split('-'))
        rng2 = tuple(int(num) for num in rng2.split('-'))
        req[field_name].append(rng1)
        req[field_name].append(rng2)

    # my ticket
    my_ticket: List[int] = [int(num) for num in raw_lst[1].strip().split('\n')[1].split(',')]

    # nearby tickets
    for ticket in raw_lst[2].strip().split('\n')[1:]:
        nearby_tickets.append([int(t) for t in ticket.split(',')])

    return req, my_ticket, nearby_tickets


# req, my_ticket, nearby_tickets = parse_input('data/day16_data')


def is_in_range(num: int, rng: Tuple[int, int]) -> bool:
    if rng[0] <= num <= rng[1]:
        return True
    return False


def error_rate(req: Dict[str, List[Tuple[int, int]]], nearby_tickets: List[List[int]]) -> int:
    ranges: List[Tuple[int, int]] = [tup for rng_line in req.values() for tup in rng_line]
    return sum(num for ticket in nearby_tickets for num in ticket if not any(is_in_range(num, rg) for rg in ranges))

# test
# assert error_rate(req, nearby_tickets) == 71
# print(error_rate(req, nearby_tickets))


## Part 2 ##

def discard_invalid_tickets(req: Dict[str, List[Tuple[int, int]]], nearby_tickets: List[List[int]]) -> List[List[int]]:
    ranges: List[Tuple[int, int]] = [tup for rng_line in req.values() for tup in rng_line]
    ticket_to_discard: List[int] = []
    for i, ticket in enumerate(nearby_tickets):
        for num in ticket:
            if not any(is_in_range(num, rng) for rng in ranges):
                ticket_to_discard.append(i)
                break
    return [ticket for i, ticket in enumerate(nearby_tickets) if i not in ticket_to_discard]


def is_in_double_range(num: int, ranges: List[Tuple[int, int]]):
    if any(is_in_range(num, rng) for rng in ranges):
        return True
    return False

# Once there are only valid tickets:
def get_fields_order(req: Dict[str, List[Tuple[int, int]]],
                     nearby_tickets: List[List[int]],
                     my_ticket: List[int]) -> List[str]:
    nearby_tickets_new = discard_invalid_tickets(req, nearby_tickets)
    fields: List[str] = []
    nearby_tickets_new.append(my_ticket)
    # transpose
    nearby_tickets_t = [[row[j] for row in nearby_tickets_new] for j in range(len(nearby_tickets_new[0]))]
    # candidates[i] is the field possibilities for the ith position
    candidates: List[Set[str]] = [set() for _ in range(len(nearby_tickets_t))]

    for field, ranges in req.items():
        for i, col in enumerate(nearby_tickets_t):
            if all(is_in_double_range(num, ranges) for num in col):
                candidates[i].add(field)
    while True:
        unique_fields = [field for candidate in candidates if len(candidate) == 1 for field in candidate]
        if len(unique_fields) == len(req):
            return [field for candidate in candidates for field in candidate]
        else:
            for i in range(len(req)):
                candidate = candidates[i]
                if len(candidate) > 1:
                    candidate = {field for field in candidate if field not in unique_fields}
                    candidates[i] = candidate

# test 0
# req, my_ticket, nearby_tickets = parse_input('data/day16_test')
# print(discard_invalid_tickets(req, nearby_tickets))
# test 1
# req, my_ticket, nearby_tickets = parse_input('data/day16_test1')


def mult_departure(my_ticket: List[int], fields: List[str]) -> int:
    departure_indices = [i for i, field in enumerate(fields) if field.startswith('departure')]
    departure_values = [my_ticket[i] for i in departure_indices]
    return reduce((lambda x, y: x * y), departure_values)


req, my_ticket, nearby_tickets = parse_input('data/day16_data')
fields = get_fields_order(req, nearby_tickets, my_ticket)
print(mult_departure(my_ticket, fields))