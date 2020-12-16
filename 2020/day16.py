from utils import api
import re

YEAR, DAY = 2020, 16


class Interval:
    def __init__(self, min_, max_):
        self.min_ = int(min_)
        self.max_ = int(max_)

    def included(self, value):
        return self.min_ <= value <= self.max_


class Field:
    pattern = re.compile(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)')

    def __init__(self, line):
        g = Field.pattern.match(line).groups()
        self.field_name = g[0]
        self.intervals = [Interval(g[1], g[2]), Interval(g[3], g[4])]

    def included(self, value):
        for interval in self.intervals:
            if interval.included(value):
                return True
        return False


def parse_input(data):
    fields = []
    for row in data:
        if Field.pattern.match(row):
            fields.append(Field(row))
        if row == 'your ticket:':
            break

    your_index = data.index('your ticket:')
    assert your_index >= 0
    your_ticket = list(map(int, data[your_index+1].split(",")))

    nearby_index = data.index('nearby tickets:')
    assert nearby_index >= 0
    tickets = []
    for index in range(nearby_index+1, len(data)):
        tickets.append(list(map(int, data[index].split(","))))

    return fields, your_ticket, tickets


def part1(data):
    fields, _, tickets = parse_input(data)

    error_rate = 0
    for ticket in tickets:
        for value in ticket:
            for field in fields:
                if field.included(value):
                    break
            else:
                error_rate += value

    return error_rate


def part2(data):
    fields, your_ticket, tickets = parse_input(data)
    invalid_tickets = []
    for ticket in tickets:
        for value in ticket:
            for field in fields:
                if field.included(value):
                    break
            else:
                invalid_tickets.append(ticket)
    for invalid in invalid_tickets:
        tickets.remove(invalid)

    all_tickets = [your_ticket]
    all_tickets.extend(tickets)

    possible_field_index = {}
    number_of_fields = len(your_ticket)
    for field in fields:
        for field_index in range(number_of_fields):
            for ticket in all_tickets:
                if not field.included(ticket[field_index]):
                    break
            else:
                if field not in possible_field_index:
                    possible_field_index[field] = []
                possible_field_index[field].append(field_index)
    field_indexes = {}
    while len(possible_field_index) > 0:
        for field in fields:
            if field in possible_field_index and len(possible_field_index[field]) == 1:
                i = possible_field_index[field][0]
                field_indexes[field] = i
                del possible_field_index[field]
                for key, value in possible_field_index.items():
                    if i in value:
                        value.remove(i)
    result = 1
    for field, index in field_indexes.items():
        if field.field_name.startswith('departure'):
            result *= your_ticket[index]
    return result


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 30869

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 4381476149273


solve()
