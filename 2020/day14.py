from utils import api
import re

YEAR, DAY = 2020, 14


class Mask:
    def __init__(self, string):
        self.mask = string
        self.set_bits = int(string.replace("X", "0"), 2)
        self.clear_bits = int(string.replace("1", "X").replace("0", "1").replace("X", "0"), 2)

    def apply_mask(self, value):
        value = value & ~self.clear_bits
        value = value | self.set_bits
        return value


def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)


def set_bit(value, bit_index):
    return value | (1 << bit_index)


def part1(data):
    pattern = re.compile(r'mem\[(\d+)\] = (\w+)')
    memory = {}
    mask = None
    for row in data:
        if row.startswith('mask = '):
            mask = Mask(row[len('mask = '):])
        else:
            groups = pattern.match(row).groups()
            address = int(groups[0])
            value = int(groups[1])
            memory[address] = mask.apply_mask(value)

    return sum(memory.values())


def get_addresses(mask, address):
    addresses = [address]
    for index in range(len(mask)):
        bit_index = len(mask) - 1 - index
        if mask[index] == 'X':
            extend = []
            for a_index in range(len(addresses)):
                extend.append(clear_bit(int(addresses[a_index]), bit_index))
                addresses[a_index] = set_bit(int(addresses[a_index]), bit_index)
            addresses.extend(extend)
        elif mask[index] == '1':
            for a_index in range(len(addresses)):
                addresses[a_index] = set_bit(int(addresses[a_index]), bit_index)
    return addresses


def part2(data):
    pattern = re.compile(r'mem\[(\d+)\] = (\w+)')
    memory = {}
    mask = None
    for row in data:
        if row.startswith('mask = '):
            mask = row[len('mask = '):]
        else:
            groups = pattern.match(row).groups()
            address = int(groups[0])
            value = int(groups[1])
            addresses = get_addresses(mask, address)
            for a in addresses:
                memory[a] = value

    return sum(memory.values())


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 15919415426101

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 3443997590975


solve()
