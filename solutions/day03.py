from utils.solution_base import SolutionBase
import re, math


class Solution(SolutionBase):
    def part1(self, data):
        nums, symbols = self.parse_input(data)
        adj_nums = []

        for pos, _ in symbols.items():
            r, c = pos
            # adj_pos = [(r + x, c + y) for x, y in itertools.product([-1, 0, 1], repeat=2)]
            adj_pos = [(r + x, c + y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
            adj_nums.extend([nums[pos] for pos in adj_pos if pos in nums])

        return sum(item[0] for item in set(adj_nums))

    def part2(self, data):
        nums, symbols = self.parse_input(data)
        _sums = 0

        for pos, symbol in symbols.items():
            if symbol == "*":
                r, c = pos
                adj_pos = [(r + x, c + y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
                adj_nums = set([nums[pos] for pos in adj_pos if pos in nums])
                if len(adj_nums) == 2:
                    _sums += math.prod([item[0] for item in adj_nums])

        return _sums

    def parse_input(self, data):
        nums = {}
        syms = {}
        idx_num = 0

        for r, line in enumerate(data):
            line_nums = re.sub(r"\D", " ", line).split()
            offset = 0
            for n in line_nums:
                pos = line.index(n, offset)
                for step in range(len(n)):
                    nums[(r, pos + step)] = (int(n), idx_num)
                offset = pos + len(n)
                idx_num += 1

            line_syms = re.sub(r"[\d\.]", " ", line).split()
            offset = 0
            for sym in line_syms:
                pos = line.index(sym, offset)
                syms[(r, pos)] = sym
                offset = pos + 1

        return nums, syms
