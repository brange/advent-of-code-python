from utils import api
import re

YEAR, DAY = 2020, 4


def parse(data):
    credentials = []
    credential = {}
    credentials.append(credential)
    for row in data.split("\n"):
        if row == '':
            credential = {}
            credentials.append(credential)
            continue
        for key_value in row.split(" "):
            key, value = key_value.split(":")
            credential[key] = value

    return credentials


def valid_data(key, value):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if key == 'byr':
        return value.isdigit() and 1920 <= int(value) <= 2002
    if key == 'iyr':
        return value.isdigit() and 2010 <= int(value) <= 2020
    if key == 'eyr':
        return value.isdigit() and 2020 <= int(value) <= 2030
    if key == 'hgt':
        pattern = re.compile(r"(\d+)(\w+)")
        match = pattern.match(value)
        if match:
            g = match.groups()
            v = int(g[0])
            return (g[1] == 'cm' and 150 <= v <= 193) or \
                   (g[1] == 'in' and 59 <= v <= 76)
        return 0
    if key == 'hcl':
        return re.compile(r'^#[a-f0-9]{6}$').match(value)
    if key == 'ecl':
        return len(value) == 3 and value in "amb blu brn gry grn hzl oth".split(" ")
    if key == 'pid':
        return re.compile(r'^\d{9}$').match(value)
    if key == 'cid':
        return True

    raise ValueError("Invalid key {}".format(key))


def count_passwords(data):
    valid_passports_p1, valid_passports_p2 = 0, 0
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for passport in data:
        for req in required:
            if req not in passport.keys():
                break
        else:
            valid_passports_p1 += 1

            for key, value in passport.items():
                if not valid_data(key, value):
                    break
            else:
                valid_passports_p2 += 1

    return valid_passports_p1, valid_passports_p2


def test():
    assert valid_data('byr', '2002')
    assert not valid_data('byr', '2003')

    assert valid_data('hgt', '60in')
    assert valid_data('hgt', '190cm')
    assert not valid_data('hgt', '190in')
    assert not valid_data('hgt', '190')

    assert valid_data('hcl', '#123abc')
    assert not valid_data('hcl', '#123abz')
    assert not valid_data('hcl', '123abc')

    assert valid_data('ecl', 'brn')
    assert not valid_data('ecl', 'wat')

    assert valid_data('pid', '000000001')
    assert not valid_data('pid', '0123456789')

    assert valid_data('cid', 'whatever')
    assert valid_data('cid', '')


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = parse(input_)
    test()

    p1, p2 = count_passwords(data)
    print("Part one {}".format(p1))
    print("Part two {}".format(p2))

    assert p1 == 200
    assert p2 == 116


solve()
