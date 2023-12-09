from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        res = 0

        for line in data:
            history = [*map(int, line.split())]
            diff = [b - a for a, b in zip(history, history[1:])]

            seqs = [history, diff]
            check = sum(1 for i in diff if i)

            while check:
                next_diff = [b - a for a, b in zip(diff, diff[1:])]
                seqs.append(next_diff)
                diff = next_diff
                check = sum(1 for i in diff if i)

            next_value = 0
            for seq in seqs[::-1]:
                next_value += seq[-1]

            res += next_value

        return res

    def part2(self, data):
        res = 0

        for line in data:
            history = [*map(int, line.split())]
            diff = [b - a for a, b in zip(history, history[1:])]

            seqs = [history, diff]
            check = sum(1 for i in diff if i)

            while check:
                next_diff = [b - a for a, b in zip(diff, diff[1:])]
                seqs.append(next_diff)
                diff = next_diff
                check = sum(1 for i in diff if i)

            next_value = 0
            for seq in seqs[::-1]:
                next_value = seq[0] - next_value

            res += next_value

        return res
