from __future__ import annotations

from typing import NamedTuple, List, Optional, Tuple

from collections import deque


class Rule(NamedTuple):
    value: int
    char: Optional[str] = None
    subrules: List[List[int]] = []


    @staticmethod
    def parse(line: str) -> Rule:
        rule_id, rest = line.split(': ')
        if rest.startswith('"'):
            return Rule(value=int(rule_id), char=rest[1:-1])

        if " | " in rest:
            rules = rest.split(" | ")
        else:
            rules = [rest]
        return Rule(value=int(rule_id),
                    subrules=[[int(n) for n in part.split(" ")] for part in rules])


def parse_input(file: str) -> Tuple[List[Rule], List[str]]:
    with open(file, 'r') as f:
        raw = f.read()
    raw_rules, raw_messages = raw.split('\n\n')
    rules: List[Rule] = [Rule.parse(line) for line in raw_rules.split('\n')]
    rules.sort()
    assert all(rule.value == i for i, rule in enumerate(rules))
    messages: List[str] = raw_messages.split('\n')
    return rules, messages


rules, messages = parse_input('data/day19_data')
rules[8] = Rule.parse("8: 42 | 42 8")
rules[11] = Rule.parse("11: 42 31 | 42 11 31")

def check(s: str, rules: List[Rule]) -> bool:
    q = deque([(s, [0])])

    while q:
        s, rule_ids = q.popleft()

        if not s and not rule_ids:
            return True
        elif not s or not rule_ids:
            continue
        elif len(rule_ids) > len(s):
            continue

        rule = rules[rule_ids[0]]
        rule_ids = rule_ids[1:]

        if rule.char and s[0] == rule.char:
            q.append((s[1:], rule_ids))
        else:
            for subrule_ids in rule.subrules:
                q.append((s, subrule_ids + rule_ids))
    return False

valid = 0
for s in messages:
    if check(s, rules):
        valid += 1

print(valid)

"""
This one was too tough to figure out in a reasonable amount of time, took help from other solution.
"""