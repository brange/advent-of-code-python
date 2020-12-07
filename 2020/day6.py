from utils import api

YEAR, DAY = 2020, 6


def part1(data):
    groups = list()
    yes_in_group = set()
    groups.append(yes_in_group)
    for row in data:
        if row == '':
            yes_in_group = set()
            groups.append(yes_in_group)
        else:
            for q in row:
                yes_in_group.add(q)

    part1 = 0
    for group in groups:
        part1 += len(group)

    return part1


class Group:
    def __init__(self):
        self.number_of_members = 0
        self.questions = {}


def part2(data):
    groups = list()
    group = Group()
    groups.append(group)
    for row in data:
        if row == '':
            group = Group()
            groups.append(group)
        else:
            group.number_of_members += 1
            for q in row:
                if q not in group.questions:
                    group.questions[q] = 0
                group.questions[q] += 1

    part2 = 0
    for g in groups:
        for q, number in g.questions.items():
            if number == g.number_of_members:
                part2 += 1

    return part2


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))


solve()
