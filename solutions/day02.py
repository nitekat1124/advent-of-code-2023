from utils.solution_base import SolutionBase
import math


class Solution(SolutionBase):
    def part1(self, data):
        thresholds = {"red": 12, "green": 13, "blue": 14}
        possibles = 0

        for line in data:
            game_info, sets = line.split(": ")
            groups = map(str.split, sets.replace(";", ",").split(", "))
            if all(int(cube_nums) <= thresholds[cube_color] for cube_nums, cube_color in groups):
                possibles += int(game_info.split(" ")[1])

        return possibles

    def part2(self, data):
        _sum = 0

        for line in data:
            counts = {"red": 0, "green": 0, "blue": 0}

            _, sets = line.split(": ")
            sets = sets.split("; ")

            for _set in sets:
                _set = {k: int(v) for v, k in map(str.split, _set.split(", "))}
                counts = {k: max(v, _set.get(k, 0)) for k, v in counts.items()}
            _sum += math.prod(counts.values())

        return _sum
