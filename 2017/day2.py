from utils import api
import sys


def part_one(cells):
    max_ = 0
    min_ = sys.maxsize
    for c in cells:
        c = int(c)
        if c > max_:
            max_ = c
        if c < min_:
            min_ = c
    return max_ - min_


def part_two(cells):
    for c1 in cells:
        for c2 in cells:
            if c1 != c2:
                div = int(c1)/int(c2)
                if int(div) == div:
                    return int(div)


data = api.fetch(2017, 2)

part1 = part2 = 0
for row in data.split("\n"):
    cells = row.split("\t")
    part1 += part_one(cells)

    part2 += part_two(cells)

print("Part one {}".format(part1))
print("Part two {}".format(part2))