"""
Represent as graph and then count along path
"""
from __future__ import annotations

from typing import List, Tuple, Dict, NamedTuple, Optional


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


WeightedGraph = List[List[Tuple[Bag, int]]]
mapping_dict: Dict[str, int] = {}


def parse_data(file: str) -> Tuple[Dict[str, Bag], int]:
    bag_id: int = 0
    bags_dict: Dict[str, Bag] = {}
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


def make_bags_graph(file: str) -> Tuple[WeightedGraph, Dict[str, Bag], int]:
    bags_dict, num_bags = parse_data(file)
    result_graph: WeightedGraph = [[] for _ in range(num_bags)]
    reversed_mapping: Dict[int, str] = {v: k for k, v in mapping_dict.items()}
    for bag_name, bag_instance in bags_dict.items():
        if bag_instance.edges:
            for edge in bag_instance.edges:
                result_graph[bag_instance.bag_id].append((bags_dict[reversed_mapping[edge.contains_bag]], edge.quantity))
    return result_graph, bags_dict, num_bags


g: WeightedGraph
num_bags: int
bags_dict: Dict[str, Bag]
g, bags_dict, num_bags = make_bags_graph('data/day7_test')
reversed_mapping: Dict[int, str] = {v: k for k, v in mapping_dict.items()}
target_count = 0
count_nodes = 0


# Depth-First-Search
def dfs(g: WeightedGraph, target: int, bag_id: int) -> None:
    global target_count
    global count_nodes
    bag: Bag = bags_dict[reversed_mapping[bag_id]]

    if not bag.seen:
        bag.seen = True
        if bag.bag_id != target:
            for edge in bag.edges:
                if bags_dict[reversed_mapping[edge.contains_bag]].contains_target and bags_dict[reversed_mapping[edge.contains_bag]].bag_id != target:
                    bag.contains_target = True
                if not bags_dict[reversed_mapping[edge.contains_bag]].seen:
                    if bags_dict[reversed_mapping[edge.contains_bag]].bag_id != target:
                        count_nodes += 1
                        dfs(g, target, bags_dict[reversed_mapping[edge.contains_bag]].bag_id)
                    else:
                        count_nodes += 1
                        bag.contains_target = True
                        target_count += count_nodes
                        count_nodes = 0
            count_nodes = 0
            if any(bags_dict[reversed_mapping[edge.contains_bag]].contains_target for edge in bag.edges):
                bag.contains_target = True


def count_containers_of(target_bag: str) -> Optional[int]:
    global target_count
    global count_nodes
    try:
        target_bag_id: int = mapping_dict[target_bag]
    except KeyError:
        print(f"Bag {target_bag} not found in mapping")
        return None
    for bag_id in range(num_bags):
        if (g[bag_id] is not None) and (not bags_dict[reversed_mapping[bag_id]].seen) and (bags_dict[reversed_mapping[bag_id]].bag_id != target_bag_id):
            count_nodes = 0
            dfs(g, target_bag_id, bag_id)
    return sum(bag.contains_target for bag in bags_dict.values())

# for test
# assert count_containers_of('shiny gold') == 4
# assert count_containers_of('muted yellow') == 2

#print(count_containers_of('shiny gold'))
#print(count_containers_of('muted yellow'))


"""
The following is some history of attempts
"""

# # Part 2 #
# bags_count = 0
# bag_accum = 0
# num_target_edges = 0
# bags_accumulator: List[int] = []
# new_bags_accumulator: List[int] = []
# extension_list: List[int] = []
# target = 0
# went_through_target: bool = False
#
# def accumulate_helper(lst: List[int]) -> int:
#     return lst[0] + (lst[0] * sum(lst[1:]))
#
#
# def dfs2(g: WeightedGraph, bag_id: int) -> int:
#     global bags_count
#     global bag_accum
#     global bags_accumulator
#     global new_bags_accumulator
#     global extension_list
#     global target
#     global went_through_target
#
#     bag: Bag = bags_dict[reversed_mapping[bag_id]]
#
#     #if not bag.seen:
#     #    bag.seen = True
#     for edge in bag.edges:
#         if bag.bag_id == target:
#             if new_bags_accumulator:
#                 extension_list.extend(new_bags_accumulator)
#                 bags_count += accumulate_helper(extension_list)
#                 new_bags_accumulator = []
#                 extension_list = []
#                 went_through_target = True
#             #bags_count += sum([*accumulate(extension_list, lambda a, b: a * b)])
#         #if not bags_dict[reversed_mapping[edge.contains_bag]].seen:
#         #if bags_dict[reversed_mapping[edge.contains_bag]].bag_id != target:
#         bags_accumulator.append(edge.quantity)
#         #print("edge.quantity: ", edge.quantity)
#         print(bag_accum)
#         bag_accum += edge.quantity + (edge.quantity * dfs2(g, bags_dict[reversed_mapping[edge.contains_bag]].bag_id))
#         #bags_count += edge.quantity * dfs2(g, bags_dict[reversed_mapping[edge.contains_bag]].bag_id)
#         #bags_count += edge.quantity + (edge.quantity * dfs2(g, bags_dict[reversed_mapping[edge.contains_bag]].bag_id))
#         #bag_accum += edge.quantity + (edge.quantity * dfs2(g, bags_dict[reversed_mapping[edge.contains_bag]].bag_id))
#         #dfs2(g, bags_dict[reversed_mapping[edge.contains_bag]].bag_id)
#     #bags_count += bag_accum
#     #bag_accum = 0
#     #new_bags_accumulator.extend([*accumulate(bags_accumulator, lambda a, b: a*b)])
#     new_bags_accumulator.extend(bags_accumulator)
#     if bag.bag_id == target:
#         if new_bags_accumulator:
#             extension_list.extend(new_bags_accumulator)
#             if went_through_target:
#                 bags_count += accumulate_helper(extension_list)
#             else:
#                 bags_count += sum([*accumulate(extension_list, lambda a, b: a*b)])
#             extension_list = []
#             new_bags_accumulator = []
#     bags_accumulator = []
#     return bag_accum
#
#
# def count_bags_contained_in(target_bag: str) -> Optional[int]:
#     global bags_count
#     global num_target_edges
#     bags_count_total = 0
#     global target
#     try:
#         target = mapping_dict[target_bag]
#         target_bag_id: int = mapping_dict[target_bag]
#     except KeyError:
#         print(f"Bag {target_bag} not found in mapping")
#         return None
#     target_edges_quantities = [q.quantity for q in bags_dict[reversed_mapping[target_bag_id]].edges]
#     first_level_bags = [bags_dict[reversed_mapping[edge.contains_bag]] for edge in bags_dict[reversed_mapping[target_bag_id]].edges]
#     num_target_edges = len(bags_dict[reversed_mapping[target_bag_id]].edges)
#     if g[target_bag_id] is not None:
#         dfs2(g, target_bag_id)
#         #for i, first_leve_edge_bag in enumerate(first_level_bags):
#             #bags_count = 0
#             #bags_count_total += dfs2(g, first_leve_edge_bag.bag_id)
#             #bags_count_total += target_edges_quantities[i] + (target_edges_quantities[i] * dfs2(g, first_leve_edge_bag.bag_id))  #dfs2(g, target_bag_id))
#     #if num_target_edges > 1:
#     #    bags_count -= sum(target_edges_quantities)
#     return bags_count
#
# # for test
# #assert count_bags_contained_in('shiny gold') == 32
# print(count_bags_contained_in('bright white'))
# # for part2_test2
# #print(count_bags_contained_in('shiny gold'))