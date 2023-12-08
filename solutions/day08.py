from utils.solution_base import SolutionBase
import math


class Solution(SolutionBase):
    def part1(self, data):
        inst = list(data[0])
        _map = {}
        for line in data[2:]:
            node, nexts = line.split(" = ")
            _map[node] = {k: v for k, v in zip(["L", "R"], nexts[1:-1].split(", "))}

        curr = "AAA"
        end = "ZZZ"
        inst_idx = 0
        steps = 0

        while curr != end:
            curr = _map[curr][inst[inst_idx]]
            inst_idx = (inst_idx + 1) % len(inst)
            steps += 1

        return steps

    def part2(self, data):
        inst = list(data[0])
        _map = {}
        for line in data[2:]:
            node, nexts = line.split(" = ")
            _map[node] = {k: v for k, v in zip(["L", "R"], nexts[1:-1].split(", "))}

        curr = [node for node in _map.keys() if node.endswith("A")]
        inst_idx = 0
        steps = 0

        least_steps = [0] * len(curr)

        while 0 in least_steps:
            for i, node in enumerate(curr):
                if node.endswith("Z") and least_steps[i] == 0:
                    least_steps[i] = steps

            curr = [_map[node][inst[inst_idx]] for node in curr]
            inst_idx = (inst_idx + 1) % len(inst)
            steps += 1

        return math.lcm(*least_steps)
