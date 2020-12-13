from utils import api
import math

YEAR, DAY = 2020, 13


class Bus:
    def __init__(self, bus_id, delay):
        self.bus_id = bus_id
        self.delay = delay


def part1(data):
    start_time = int(data[0])
    schedule = list()
    for a in data[1].split(","):
        if a == 'x':
            continue
        schedule.append(int(a))
    first_possibles = []
    for a in schedule:
        b = math.ceil(start_time / a) * a
        if b < a:
            b += a
        first_possibles.append(b)
    first_bus = first_possibles.index(min(first_possibles))
    return (min(first_possibles)-start_time) * schedule[first_bus]


def part2(data):
    buses = list()
    index = -1
    line = data[1]
    for a in line.split(","):
        index += 1
        if a == 'x':
            continue
        buses.append(Bus(int(a), index))

    t = buses[0].bus_id
    t_delta = buses[0].bus_id
    for a in range(1, len(buses)):
        while True:
            all_good = True
            buses_sliced = buses[:a + 1]
            for bus in buses_sliced:
                if (t + bus.delay) % bus.bus_id != 0:
                    all_good = False
                    break
            if all_good:
                t_delta = math.lcm(*list(map(lambda x: x.bus_id, buses_sliced)))
                break
            else:
                t += t_delta

    return t


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 119
    assert p2 == 1106724616194525


solve()
