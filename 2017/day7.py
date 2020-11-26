from utils import api
import re

data = api.fetch(2017, 7)


class Program:
    def __init__(self, name, weight):
        self.name = name
        self.children = []
        self.parent = None
        self.weight = weight

    def __str__(self):
        return "name: {}, parent: {}, children: {}".format(self.name,
                                                           self.parent.name if self.parent is not None else "None",
                                                           self.children)


def calculate_weight(program, all_programs):
    w = program.weight
    for c in program.children:
        p = all_programs[c]
        w += calculate_weight(p, all_programs)
    return w


def trim(x):
    return x.strip()


def solve():
    programs = {}
    pattern = re.compile(r"(\w+) \((\d+)\)[ ->]*([a-z, ]+)*")
    for row in data.split("\n"):
        groups = pattern.match(row).groups()
        name = groups[0]
        programs[name] = Program(name, int(groups[1]))

        if len(groups) == 3 and groups[2] is not None:
            programs[name].children = list(map(trim, groups[2].split(",")))

    for _, child in programs.items():
        for _, parent in programs.items():
            if child.name in parent.children:
                child.parent = parent
                break

    root = None
    for _, program in programs.items():
        if program.parent is None:
            root = program
            break
    print("Part one: {}".format(root))
    assert root is not None
    assert root.name == 'cyrupz'

    def is_children_balanced(program, all_programs):
        w_ = set()
        for c_ in program.children:
            child = all_programs[c_]
            w_.add(calculate_weight(child, all_programs))
        return len(w_) == 1

    def part2(program, all_programs):
        weights = {}
        for c_ in program.children:
            child = all_programs[c_]
            w = calculate_weight(child, all_programs)
            if w not in weights:
                weights[w] = []
            weights[w].append(child)

        assert len(weights) == 2

        wrong_one, another_one, wrong_weight, right_weight = None, None, 0, 0
        for weight, children in weights.items():
            if len(children) == 1:
                wrong_one = children[0]
                wrong_weight = weight
            else:
                another_one = children[0]
                right_weight = weight

        assert wrong_one is not None and another_one is not None

        if is_children_balanced(wrong_one, all_programs):
            print("Part two, {} weight should be {} instead of {}".format(wrong_one.name,
                                                                          wrong_one.weight - (wrong_weight - right_weight),
                                                                          wrong_one.weight))
        else:
            part2(wrong_one, all_programs)

    part2(root, programs)


solve()
