from utils import api

YEAR, DAY = 2020, 10


def part1(data):
    current_joltage = 0
    ones, threes = 0, 0
    while len(data) > 0:
        next_adapter = min(data)
        data.remove(next_adapter)
        diff = next_adapter - current_joltage
        current_joltage = next_adapter
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1
        else:
            raise RuntimeError("Invalid diff {}".format(diff))
    threes += 1 # For the device
    print("ones {} threes {}".format(ones, threes))
    return ones * threes


class Adapter:
    def __init__(self, joltage):
        self.joltage = joltage
        self.children = []
        self.total_number_of_children = 0


def part2(data):
    device_voltage = max(data) + 3
    adapters = {}
    for joltage in data:
        adapters[joltage] = Adapter(joltage)

    for joltage, adapter in adapters.items():
        for diff in range(1, 4):
            if (diff + joltage) in adapters:
                adapter.children.append(adapters[diff + joltage])

    adapters[max(data)].children.append(Adapter(device_voltage))
    adapters[max(data)].total_number_of_children = 1

    for joltage in reversed(sorted(data)):
        adapter = adapters[joltage]
        for child in adapter.children:
            adapter.total_number_of_children += child.total_number_of_children
    sum_ = 0
    for a in range(1, 4):
        if a in adapters:
            sum_ += adapters[a].total_number_of_children
    return sum_


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")
    data = list(map(int, data))

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    data = input_.strip().split("\n")
    data = list(map(int, data))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 2201
    assert p2 == 169255295254528


_, t = api.time_it(solve)
print("Total time {} ms".format(t))
