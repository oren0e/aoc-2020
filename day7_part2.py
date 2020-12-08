"""
Represent as tree and then count along path
"""
from __future__ import annotations

from typing import List, Tuple, Dict, NamedTuple


class Edge(NamedTuple):     # represents the relation "contains"
    quantity: int
    contains_bag: int


class Bag:
    def __init__(self, bag_id: int, bag_name: str) -> None:
        self.bag_id = bag_id
        self.bag_name = bag_name
        self.edges: List[Edge] = []
        self.seen: bool = False
        self.contains_target: bool = False

    def __repr__(self) -> str:
        return repr(f"Bag(bag_id:{self.bag_id}, bag_name:{self.bag_name}, seen: {self.seen},"
                    f" contains_target:{self.contains_target} \n"
                    f"Edges: {self.edges})")


mapping_dict: Dict[str, int] = {}


def parse_data(file: str) -> Tuple[Dict[str, Bag], int]:
    bag_id: int = 0
    bags_dict: Dict[str, Bag] = {}  # {Bag: bag_id}
    with open(file, 'r') as f:
        for num_bags, line in enumerate(f):
            relation: List[str] = line.strip().replace('bags contain', '*')\
                .replace('bags', '*')\
                .replace('bag','*')\
                .replace(',', '')\
                .replace('.','')\
                .split('*')
            for i, row in enumerate(relation):
                striped_row = row.strip()
                if striped_row == '':
                    break
                if striped_row == 'no other':
                    continue
                if i == 0:  # the first bag (that has all the relations with)
                    if striped_row not in mapping_dict:
                        mapping_dict[striped_row] = bag_id
                        bag_instance = Bag(mapping_dict[striped_row], bag_name=striped_row)
                        bags_dict[striped_row] = bag_instance
                        bag_id += 1
                    else:
                        bag_instance = bags_dict[striped_row]
                else:
                    bag: str = ' '.join(striped_row.split()[1:])
                    weight: int = int(striped_row.split()[0])

                    if bag in bags_dict:
                        edge = Edge(quantity=weight, contains_bag=bags_dict[bag].bag_id)
                        bag_instance.edges.append(edge)
                    else:
                        if bag not in mapping_dict:
                            mapping_dict[bag] = bag_id
                            bags_dict[bag] = Bag(mapping_dict[bag], bag_name=bag)
                            bag_id += 1
                        edge = Edge(quantity=weight, contains_bag=bags_dict[bag].bag_id)
                        bag_instance.edges.append(edge)
    return bags_dict, num_bags + 1


bags_dict, num_bags = parse_data('data/day7_data')
reversed_mapping: Dict[int, str] = {v: k for k, v in mapping_dict.items()}

bags_container: Dict[str, List[str]] = {}
for k, v in bags_dict.items():
    bags_container[k] = []
    try:
        for edge in v.edges:
            edge_bag = bags_dict[reversed_mapping[edge.contains_bag]]
            bags_container[k] += [edge_bag.bag_name] * edge.quantity
    except:
        pass


def count_bags_in(my_bag: str) -> int:
    if my_bag == " " or bags_container.get(my_bag) is None:
        return 0
    cnt = len(bags_container[my_bag])
    counts = []
    for item in bags_container[my_bag]:
        counts.append(count_bags_in(item))
    return sum(counts) + cnt

print(count_bags_in('shiny gold'))