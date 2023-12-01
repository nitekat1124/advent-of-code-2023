from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        _sum = 0
        for line in data:
            digits = [int(i) for i in line if i.isdigit()]
            _sum += digits[0] * 10 + digits[-1]
        return _sum

    def part2(self, data):
        mappings = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

        new_data = [[x if (x := "".join([v for k, v in mappings.items() if line[i:].startswith(k)])) else line[i] for i in range(len(line))] for line in data]
        return self.part1(new_data)
