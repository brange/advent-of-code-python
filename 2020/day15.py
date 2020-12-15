from utils import api

YEAR, DAY = 2020, 15


def part1(data, last_turn=2020):
    turn = 0
    memory = {}
    last_spoken = None
    init_numbers = list(map(int, data.split(",")))
    for init in init_numbers:
        turn += 1
        last_spoken = turn - memory[init] if init in memory else 0
        memory[init] = turn

    while True:
        turn += 1
        ls = last_spoken
        last_spoken = turn - memory[last_spoken] if last_spoken in memory else 0
        memory[ls] = turn
        if turn == last_turn:
            return ls


def part2(data):
    return part1(data, 30000000)


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip()

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 758
    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 814


solve()
