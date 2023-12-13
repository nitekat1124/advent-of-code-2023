from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        maps = ("\n".join(data)).split("\n\n")
        return sum(self.find_mirror(_map) for _map in maps)

    def part2(self, data):
        maps = ("\n".join(data)).split("\n\n")
        _sum = 0

        for _map in maps:
            ref_org = self.find_mirror(_map)
            width = len(_map.split("\n")[0])

            s = "#."
            i, j = 0, 0
            done = False

            while not done:
                pattern = _map.split("\n")
                pattern[i] = pattern[i][:j] + s[(s.index(pattern[i][j]) + 1) % 2] + pattern[i][j + 1 :]
                pattern = "\n".join(pattern)

                ref = self.find_mirror(pattern, ref_org)
                if ref > -1:
                    _sum += ref
                    done = True
                i, j = i + (j + 1) // width, (j + 1) % width

        return _sum

    def find_mirror(self, _map, ref_org=None):
        _map_h = _map.split("\n")
        _map_v = ["".join(c) for c in zip(*_map_h)]

        for pattern, weight in ((_map_h, 100), (_map_v, 1)):
            for i in range(1, len(pattern)):
                a, b = pattern[:i], pattern[i:]
                a = "".join([x for x in a[::-1]])
                b = "".join(b)
                if a.startswith(b) or b.startswith(a):
                    ref = i * weight
                    if ref != ref_org:
                        return ref

        return -1
