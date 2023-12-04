from utils.solution_base import SolutionBase
from functools import reduce  # noqa: F401


class Solution(SolutionBase):
    def part1(self, data):
        points = 0
        for line in data:
            """
            # original:
            winning, yours = line.split(":")[1].split("|")
            winning = set(winning.split())
            yours = set(yours.split())
            """

            """
            # simplified using map:
            winning, yours = map(lambda nums: set(nums.split()), line.split(":")[1].split("|"))
            """

            # more simplified:
            winning, yours = map(set, map(str.split, line.split(":")[1].split("|")))

            """
            # original:
            matched_count = len(winning & yours)
            if matched_count > 0:
                points += 2 ** (matched_count - 1)
            """

            # simplified:
            points += int(2 ** (len(winning & yours) - 1))

        """
        # one-liner
        points = sum(int(2 ** (len(set.intersection(*map(set, map(str.split, line.split(":")[1].split("|"))))) - 1)) for line in data)
        """

        return points

    def part2(self, data):
        cards = [1] * len(data)

        for i, line in enumerate(data):
            winning, yours = map(set, map(str.split, line.split(":")[1].split("|")))
            matched_count = len(winning & yours)
            for j in range(1, matched_count + 1):
                cards[i + j] += cards[i]

        """
        # one-liner
        cards = reduce(
            lambda acc, cur: [v + [0, acc[cur[0]]][cur[0] < i <= sum(cur)] for i, v in enumerate(acc)],
            [(i, len(set.intersection(*map(set, map(str.split, line.split(":")[1].split("|")))))) for i, line in enumerate(data)],
            [1] * len(data),
        )
        """
        return sum(cards)
