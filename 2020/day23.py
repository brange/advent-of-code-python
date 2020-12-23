from utils import api

YEAR, DAY = 2020, 23


class Cup:
    last_index = 0

    def __init__(self, label):
        self.label = int(label)
        Cup.last_index = self.label
        self.next = None
        self.prev = None

    def remove(self):
        self.prev.next, self.next.prev = self.next, self.prev
        return self

    def insert_after(self, cup):
        cup.next, self.next = self.next, cup
        cup.next.prev = cup
        cup.prev = self


def part2(data, is_part2=False):
    first = Cup(data[0])
    prev = first
    max_ = first.label
    one = first if first.label == 1 else None
    cup_map = {first.label: first}
    for label in data[1:]:
        c = Cup(label)
        cup_map[c.label] = c
        if c.label == 1:
            one = c
        max_ = max(c.label, max_)
        c.prev = prev
        prev.next = c
        prev = c
    if is_part2:
        for label in range(max_+1, 10**6 + 1):
            c = Cup(label)
            cup_map[c.label] = c
            max_ = max(c.label, max_)
            c.prev = prev
            prev.next = c
            prev = c
    last = prev
    last.next = first
    first.prev = last
    assert one

    current = first
    for _ in range(10**7 if is_part2 else 100):
        pickups = []
        for _ in range(3):
            pickups.append(current.next.remove())

        destination_label = current.label-1
        while destination_label in [cup.label for cup in pickups] or destination_label == 0:
            if destination_label == 0:
                destination_label = max_+1
            destination_label -= 1

        destination = cup_map[destination_label]

        current = current.next

        for p in reversed(pickups):
            destination.insert_after(p)
    if is_part2:
        print("Using {} and {} for part2".format(one.next.label, one.next.next.label))
        return one.next.label * one.next.next.label
    else:
        n = one.next
        res = ""
        while n.label != 1:
            res += str(n.label)
            n = n.next
        return res


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip()

    p1, p1_time = api.time_it(part2, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == '62934785'

    p2, p2_time = api.time_it(part2, data, True)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 693659135400

solve()
