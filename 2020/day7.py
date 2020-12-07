from utils import api

YEAR, DAY = 2020, 7


class ChildBag:
    bag_color: str

    def __init__(self, amount, bag_color):
        self.amount = amount
        self.bag_color = bag_color


class Bag:
    children: list[ChildBag]

    def __init__(self, color):
        self.color = color.strip()
        self.children = []


def parse_input(data):
    bags = {}
    for row in data:
        s = row.split("bags contain")
        b = Bag(s[0])
        bags[b.color] = b
        if s[1].strip() == "no other bags.":
            continue

        children = s[1].split(",")
        for child in children:
            amount, name = child.split("bag")[0].strip().split(" ", 1)
            b.children.append(ChildBag(int(amount), name))
    return bags


def find(target, bag, all_bags):
    for child in bag.children:
        if child.bag_color == target:
            return 1
        in_child = find(target, all_bags[child.bag_color], all_bags)
        if in_child:
            return 1
    return 0


def part1(data):
    bags = parse_input(data)
    target_bag = 'shiny gold'

    p1 = 0
    for color, bag in bags.items():
        p1 += find(target_bag, bag, bags)

    return p1


def count_children(bag, all_bags):
    number_of_bags = 0
    for child in bag.children:
        number_of_bags += child.amount * (1 + count_children(all_bags[child.bag_color], all_bags))
    return number_of_bags


def part2(data):
    bags = parse_input(data)
    target_bag = 'shiny gold'

    return count_children(bags[target_bag], bags)


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))


solve()
