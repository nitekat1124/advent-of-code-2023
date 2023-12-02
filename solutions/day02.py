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

        """
        # one-liner
        possibles = sum(i * all(int(cube_nums) <= thresholds[cube_color] for cube_nums, cube_color in map(str.split, line.split(": ")[1].replace(";", ",").split(", "))) for i, line in enumerate(data, 1))
        """

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

        """
        # one-liner
        _sum = sum(math.prod([max(map(lambda s: s.get(color, 0), [{k: int(v) for v, k in map(str.split, _set.split(", "))} for _set in line.split(": ")[1].split("; ")])) for color in ("red", "green", "blue")]) for line in data)
        """

        return _sum
