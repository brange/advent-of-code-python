from utils import api

YEAR, DAY = 2020, 25


def calculate_loop_size(subject_number, public_key):
    key = 1
    loop_size = 0
    while key != public_key:
        loop_size += 1
        key = key * subject_number
        key = key % 20201227
    return loop_size


def transform(subject_number, loop_size):
    return pow(subject_number, loop_size, 20201227)
    #key = 1
    #for _ in range(loop_size):
    #    key = key * subject_number
    #    key = key % 20201227
    #return key


def part1(data):
    card_public = int(data[0])
    door_public = int(data[1])
    card_loop_size = calculate_loop_size(7, card_public)
    return transform(door_public, card_loop_size)


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 6198540


solve()
