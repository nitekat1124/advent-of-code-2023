from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        points = 0
        for line in data:
            # winning, yours = line.split(":")[1].split("|")
            # winning = set([*map(int, winning.strip().split())])
            # yours = set([*map(int, yours.strip().split())])
            winning, yours = map(lambda nums: set(map(int, nums.strip().split())), line.split(":")[1].split("|"))

            # matched_count = len(winning & yours)
            # if matched_count > 0:
            #     points += 2 ** (matched_count - 1)
            points += int(2 ** (len(winning & yours) - 1))

        """
        # one-liner
        points = sum([int(2 ** (len(set.intersection(*map(lambda nums: set(map(int, nums.strip().split())), line.split(":")[1].split("|")))) - 1)) for line in data])
        """

        return points

    def part2(self, data):
        cards = [1] * len(data)

        for i, line in enumerate(data):
            winning, yours = map(lambda nums: set(map(int, nums.strip().split())), line.split(":")[1].split("|"))
            matched_count = len(winning & yours)
            for j in range(1, matched_count + 1):
                cards[i + j] += cards[i]

        return sum(cards)
