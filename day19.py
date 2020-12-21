from typing import List, Union, Tuple, NamedTuple, Optional

from collections import deque

import re


# class Rule(NamedTuple):
#     num: int
#     value: Union[int, str]


RuleSet = List[List[List[Union[int, str]]]]


def parse_input(file: str) -> Tuple[RuleSet, List[str]]:
    with open(file, 'r') as f:
        raw = f.read()
    split_raw = raw.split('\n\n')
    num_rules = len(split_raw[0].split('\n'))
    rules: RuleSet = [[] for _ in range(num_rules)]

    # rules
    for rule in split_raw[0].split('\n'):
        rule = rule.strip()
        num_rule = int(re.findall(r'\d+', rule)[0])
        if "|" in rule:
            try:
                first_set: List[int] = [int(num) for num in rule.split(":")[1].split("|")[0].split()]
                rules[num_rule].append(first_set)
                second_set: List[int] = [int(num) for num in rule.split(":")[1].split("|")[1].split()]
                rules[num_rule].append(second_set)
            except IndexError:
                rules[num_rule].append(first_set)  # no second set
        elif ('"a"' in rule) or ('"b"' in rule):
            first_set: str = rule.split(":")[1].split()[0].strip('"')
            rules[num_rule].append([first_set])
        else:
            first_set: List[int] = [int(num) for num in rule.split(":")[1].split()]
            rules[num_rule].append(first_set)

    # received messages
    messages = [msg.strip() for msg in split_raw[1].split('\n')]
    return rules, messages


#rules, messages = parse_input('data/day19_test2')

def crawl(rules:RuleSet, rule_to_check: int = 0) -> List[str]:
    res = []
    if rules[rule_to_check][0][0] == 'b':
        return ['b']
    elif rules[rule_to_check][0][0] == 'a':
        return ['a']

    for rule in rules[rule_to_check]:
        if len(rule) == 1:
            res += crawl(rules, rule[0])
        elif len(rule) == 2:        # this is not a general solution! (we could have 4 length rule or more)
            option1 = crawl(rules, rule[0])
            option2 = crawl(rules, rule[1])
            res += [x + y for x in option1 for y in option2]
        elif len(rule) == 3:
            option1 = crawl(rules, rule[0])
            option2 = crawl(rules, rule[1])
            option3 = crawl(rules, rule[2])
            res += [x + y + z for x in option1 for y in option2 for z in option3]

    return res


#possibilities = crawl(rules, 0)

# for test
# assert len([item for item in messages if item in possibilities]) == 2

#print(len([item for item in messages if item in possibilities]))

## Part 2 ##

class Rule(NamedTuple):
    value: int
    char: Optional[str] = None


def parse_input2(file: str) -> Tuple[RuleSet, List[str]]:
    with open(file, 'r') as f:
        raw = f.read()
    split_raw = raw.split('\n\n')
    num_rules = len(split_raw[0].split('\n'))
    rules: RuleSet = [[] for _ in range(num_rules)]

    # rules
    for rule in split_raw[0].split('\n'):
        rule = rule.strip()
        num_rule = int(re.findall(r'\d+', rule)[0])
        # replacing section
        if num_rule == 8:
            rule = "8: 42 | 42 8"
        elif num_rule == 11:
            rule = "11: 42 31 | 42 11 31"

        if "|" in rule:
            try:
                first_set: List[Rule] = [Rule(int(num)) for num in rule.split(":")[1].split("|")[0].split()]
                rules[num_rule].append(first_set)
                second_set: List[Rule] = [Rule(int(num)) for num in rule.split(":")[1].split("|")[1].split()]
                rules[num_rule].append(second_set)
            except IndexError:
                rules[num_rule].append(first_set)  # no second set
        elif ('"a"' in rule) or ('"b"' in rule):
            first_set: str = rule.split(":")[1].split()[0].strip('"')
            rules[num_rule].append([Rule(num_rule, first_set)])
        else:
            first_set: List[Rule] = [Rule(int(num)) for num in rule.split(":")[1].split()]
            rules[num_rule].append(first_set)

    # received messages
    messages = [msg.strip() for msg in split_raw[1].split('\n')]
    return rules, messages


rules, messages = parse_input2('data/day19_test')
#possibilities = crawl(rules, 0)

"""
Generating all the possibilities won't work here (because of loops).
We have to check each message against the rules. I got help from other
solutions.
"""
def check(s: str, rules: List[List[List[Rule]]]) -> bool:
    """
    Returns True if s is valid for rules[0].
    """
    q = deque([(s, [Rule(0)])])

    while q:
        s, rule_ids = q.popleft()

        if not s and not rule_ids:
            return True
        elif not s or not rule_ids:
            continue
        elif len(rule_ids) > len(s):    # each rule can only match 1 character
            continue

        rule = rules[rule_ids[0].value][0][0]
        rule_ids = rule_ids[1:]

        if rule.char and s[0] == rule.char:
            q.append((s[1:], rule_ids))
        elif rule.char and not rule_ids:
            continue
        else:
            for subrule_ids in rules[rule.value]:
                q.append((s, subrule_ids + rule_ids))
    return False

valid = 0
for i, s in enumerate(messages):
    print(i, s)
    if check(s, rules):
        valid += 1

print(valid)