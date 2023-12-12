from utils.solution_base import SolutionBase
from functools import cache


class Solution(SolutionBase):
    def part1(self, data):
        _sum = 0

        for line in data:
            springs, groups = line.split()
            groups = tuple([*map(int, groups.split(","))])
            _sum += self.get_possible_count(springs, groups)

        return _sum

    def part2(self, data):
        _sum = 0

        for line in data:
            springs, groups = line.split()

            springs = "?".join([springs] * 5)
            groups = ",".join([groups] * 5)
            groups = tuple([*map(int, groups.split(","))])

            _sum += self.get_possible_count(springs, groups)

        return _sum

    @cache
    def get_possible_count(self, springs: str, groups: tuple, prev_size=0, must_operational=False) -> int:
        # if there are no more springs left
        if springs == "":
            # if there are still groups left
            if groups:
                # if only one group left and it matches the previous counted size
                if len(groups) == 1 and groups[0] == prev_size:
                    return 1  # last group matches the previous counted size, valid
                return 0  # no springs left but still groups, impossible
            else:
                # no springs and no groups left
                if prev_size == 0:
                    return 1  # no previous size, valid
                else:
                    return 0  # impossible situation

        # no more groups left
        if len(groups) == 0:
            # if there a remaining springs, it's impossible
            if "#" in springs or prev_size > 0:
                return 0
            return 1  # no more springs, valid

        # deal with the current spring
        curr = springs[0]
        rest = springs[1:]

        # if current spring is "?", it could be either "#" or "."
        if curr == "?":
            return self.get_possible_count("#" + rest, groups, prev_size, must_operational) + self.get_possible_count("." + rest, groups, prev_size, must_operational)

        # if current spring is "#" (damaged)
        if curr == "#":
            # shouldn't be a operational spring (i.e. ".")
            if must_operational:
                return 0

            # current size
            curr_size = prev_size + 1

            # check current size against the group
            if curr_size > groups[0]:  # exceeds the group count, impossible
                return 0
            elif curr_size == groups[0]:  # matches the group count, clear the prev size, next spring must be operational
                return self.get_possible_count(rest, groups[1:], 0, True)
            else:  # current size is less than the group count, keep counting, next spring can't be operational
                return self.get_possible_count(rest, groups, curr_size, False)

        # if current spring is "." (operational)
        if curr == ".":
            # counting the rest springs
            if must_operational:
                return self.get_possible_count(rest, groups, 0, False)

            # counting the rest springs
            if prev_size == 0:
                return self.get_possible_count(rest, groups, 0, False)
            else:
                # check current size against the group
                if prev_size != groups[0]:
                    return 0  # if not match, impossible
                else:
                    # if match, clear the prev size, next spring can't be operational, counting the rest springs
                    return self.get_possible_count(rest, groups[1:], 0, False)
