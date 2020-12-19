from utils import api
import re

YEAR, DAY = 2020, 19


class Rule:
    def __init__(self, rule_number, sub_rules):
        self.rule_number = rule_number
        self.sub_rules = sub_rules


def parse_input(data):
    rules = {}
    index = 0
    for row in data:
        index += 1
        if row.strip() == '':
            break
        split = row.split(':')
        sub_rules = []
        for r in split[1].split('|'):
            sub_rules.append(r.strip().split(' '))
        rule = Rule(int(split[0]), sub_rules)
        rules[rule.rule_number] = rule

    inputs = []
    for i in range(index, len(data)):
        inputs.append(data[i])

    return rules, inputs


def build_regex(all_rules, rule_number=0, max_recursive_level=-1, recursive_level=0):
    regex = ""
    for sub_rule in all_rules[rule_number].sub_rules:
        if rule_number in sub_rule and max_recursive_level > 0 and recursive_level > max_recursive_level:
            continue
        for rule in sub_rule:
            if rule == '"a"' or rule == '"b"':
                regex += rule[1:2]
            else:
                regex += build_regex(all_rules, int(rule), max_recursive_level, recursive_level + 1)
        regex += "|"
    regex = regex[:-1]
    if len(regex) > 0:
        regex = "(" + regex + ")"
    return regex


def part1(data):
    rules, inputs = parse_input(data)

    rule0 = "^" + build_regex(rules, 0) + "$"

    pattern = re.compile(rule0)
    num_matches = 0
    for input in inputs:
        if pattern.match(input):
            num_matches += 1

    return num_matches


def part2(data):
    rules, inputs = parse_input(data)
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    rule8 = Rule(8, [[42], [42, 8]])
    rule11 = Rule(11, [[42, 31], [42, 11, 31]])
    #rule8 = Rule(8, [["42+"]])
    #rule11 = Rule(11, [["41+", "31+"]])
    rules[8] = rule8
    rules[11] = rule11

    max_input_length = 0
    for input in inputs:
        max_input_length = max(max_input_length, len(input))

    rule0 = "^" + build_regex(rules, 0, max_input_length) + "$"

    pattern = re.compile(rule0)
    num_matches = 0
    for input in inputs:
        if pattern.match(input):
            num_matches += 1

    return num_matches


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 134

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))


solve()
