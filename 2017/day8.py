from utils import api
import re
import sys


data = api.fetch(2017, 8)
registers = {}
pattern = re.compile(r"(\w+) (dec|inc) (-?\d+) if (\w+) ([=<>!]+) (-?\d+)")


def touch_register(reg):
    if reg not in registers:
        registers[reg] = 0


def compare(a, b, comparator):
    if comparator == '==':
        return a == b
    if comparator == '>=':
        return a >= b
    if comparator == '>':
        return a > b
    if comparator == '<=':
        return a <= b
    if comparator == '<':
        return a < b
    if comparator == '!=':
        return a != b


def find_max_value():
    max_reg, max_value = None, sys.maxsize * -1
    for reg, value in registers.items():
        if value > max_value:
            max_reg, max_value = reg, value
    return max_reg, max_value


def solve():
    _, max_part_2 = find_max_value()
    for row in data.split("\n"):
        groups = pattern.match(row).groups()
        reg = groups[0]
        touch_register(reg)
        multiplier = 1 if groups[1] == 'inc' else -1
        diff = int(groups[2])

        touch_register(groups[3])
        check_reg = registers[groups[3]]
        comparator = groups[4]
        check_value = int(groups[5])
        if compare(check_reg, check_value, comparator):
            registers[reg] += multiplier * diff
            if registers[reg] > max_part_2:
                max_part_2 = registers[reg]

    max_reg, max_value = find_max_value()
    print("Part one, max register is {} with value {}".format(max_reg, max_value))
    print("Part two, max memory size is {}".format(max_part_2))


solve()
