from utils import api
import re

YEAR, DAY = 2020, 2
pattern = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def parse(row):
    groups = pattern.match(row).groups()
    return int(groups[0]), int(groups[1]), groups[2], groups[3]


def part1(data):
    valid_passwords = 0
    for row in data:
        min, max, char, password = parse(row)
        appearances = password.count(char)
        if min <= appearances <= max:
            valid_passwords += 1

    return valid_passwords


def part2(data):
    valid_passwords = 0
    for row in data:
        pos_a, pos_b, char, password = parse(row)
        pos_a -= 1
        pos_b -= 1
        a = password[pos_a] == char
        b = password[pos_b] == char
        if a != b:
            valid_passwords += 1
    return valid_passwords


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 628
    assert p2 == 705

solve()
