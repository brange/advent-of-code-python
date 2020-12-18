from utils import api

YEAR, DAY = 2020, 18


def calc(row, is_part2=False, start_index=0, start_subcalc='('):
    sum_ = 0
    index = start_index
    operator = '+'
    add_or_multiply = lambda value: sum_ + value if operator == '+' else sum_ * value
    while index < len(row):
        item = row[index]
        if item == ' ':
            index += 1
            continue

        if item in '*+':
            operator = item

        if item == '(' or (is_part2 and item == '*'):
            s, index = calc(row, is_part2, index + 1, item)
            sum_ = add_or_multiply(s)
        elif item == ')' or (start_subcalc == '*' and item == '*'):
            if start_subcalc == '*' and item == ')':
                index -= 1
            return sum_, index
        elif item.isdigit():
            a = item
            while index + 1 < len(row) and row[index + 1].isdigit():
                a += row[index + 1]
                index += 1
            sum_ = add_or_multiply(int(a))
        index += 1

    return sum_, index


def calc_part2(row):
    return calc(row, True)


def test():
    assert calc("1 + 2 * 3 + 4 * 5 + 6")[0] == 71
    assert calc("1 + (2 * 3) + (4 * (5 + 6))")[0] == 51
    assert calc("2 * 3 + (4 * 5)")[0] == 26

    assert calc_part2("1 + 2 * 3 + 4 * 5 + 6")[0] == 231

    assert calc_part2("1 + (2 * 3) + (4 * (5 + 6))")[0] == 51
    assert calc_part2("2 * 3 + (4 * 5)")[0] == 46
    assert calc_part2("5 + (8 * 3 + 9 + 3 * 4 * 3)")[0] == 1445
    assert calc_part2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")[0] == 669060

    assert calc_part2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")[0] == 23340
    assert calc_part2('2 + (18) * 4')[0] == 80


def part1(data):
    sum_ = 0
    for row in data:
        sum_ += calc(row)[0]
    return sum_


def part2(data):
    sum_ = 0
    for row in data:
        sum_ += calc_part2(row)[0]
    return sum_


def solve():
    test()
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))
    assert p1 == 30753705453324

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))
    assert p2 == 244817530095503


solve()
