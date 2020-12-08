from utils import api

YEAR, DAY = 2020, 8


class Computer:
    def __init__(self):
        self.accumulator = 0
        self.index = 0
        self.visited_indexes = set()

    def execute(self, instruction, amount):
        if instruction == 'acc':
            self.acc(amount)
        elif instruction == 'jmp':
            self.jmp(amount)
        elif instruction == 'nop':
            self.nop()
        else:
            raise RuntimeError("Invalid instruction {}".format(instruction))

    def acc(self, amount):
        self.accumulator += amount
        self.index += 1

    def jmp(self, amount):
        self.index += amount

    def nop(self):
        self.index += 1

    def check_for_loop(self):
        if self.index in self.visited_indexes:
            return True
        self.visited_indexes.add(self.index)
        return False


def create_instructions(data):
    instructions = []
    for row in data:
        instruct, amount = row.split(" ")
        instructions.append((instruct, int(amount)))
    return instructions


def run_instructions(instructions):
    computer = Computer()
    while computer.index < len(instructions):
        instruction = instructions[computer.index]
        computer.execute(instruction[0], instruction[1])
        if computer.check_for_loop():
            return False, computer.accumulator
    return True, computer.accumulator


def part1(data):
    instructions = create_instructions(data)
    _, p1 = run_instructions(instructions)
    return p1


def part2(data):
    instructions = create_instructions(data)
    for index in range(len(instructions)):
        before = instructions[index]
        if before[0] == 'jmp':
            instructions[index] = ('nop', before[1])
        elif before[0] == 'nop':
            instructions[index] = ('jmp', before[1])
        else:
            continue

        exited, acc = run_instructions(instructions)
        if exited:
            return acc
        instructions[index] = before

    raise RuntimeError("part2 failed")


def solve():
    input_ = api.fetch(YEAR, DAY)
    data = input_.strip().split("\n")

    p1, p1_time = api.time_it(part1, data)
    print("Part one {}, it took {} ms".format(p1, p1_time))

    p2, p2_time = api.time_it(part2, data)
    print("Part two {}, it took {} ms".format(p2, p2_time))

    assert p1 == 1451
    assert p2 == 1160


solve()
