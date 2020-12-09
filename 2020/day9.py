from utils import api

YEAR, DAY = 2020, 9


def find_sum(preamble, target):
    for a in preamble:
        for b in preamble:
            if a + b == target:
                return True
    return False


def part1(data):
    preamble_len = 25
    preamble = list()
    for number in data:
        if len(preamble) < preamble_len:
            preamble.append(number)
        else:
            if find_sum(preamble, number):
                preamble = preamble[1:]
                preamble.append(number)
            else:
                return number


def part2(data, answer_part1):
    arr = list()
    for num in data:
        arr.append(num)
        while sum(arr) > answer_part1:
            arr = arr[1:]
        if sum(arr) == answer_part1:
            return min(arr) + max(arr)


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")
    data = list(map(int, data))

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data, p1)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 1212510616
    assert p2 == 171265123


solve()
