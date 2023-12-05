from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        seeds = [*map(int, data[0].split(": ")[1].split())]
        maps = [[[*map(int, n.split())] for n in i.split("\n")[1:]] for i in "\n".join(data[2:]).split("\n\n")]

        locations = []
        for curr in seeds:
            for _map in maps:
                for dest, src, rng in _map:
                    if src <= curr < src + rng:
                        idx = curr - src
                        curr = dest + idx
                        break
            locations.append(curr)

        return min(locations)

    def part2(self, data):
        seeds = [*map(int, data[0].split(": ")[1].split())]
        maps = [[[*map(int, n.split())] for n in i.split("\n")[1:]] for i in "\n".join(data[2:]).split("\n\n")]

        locations = []
        seed_pairs = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]
        for pair in seed_pairs:
            remain = [pair]
            result = []

            for _map in maps:
                while remain:
                    cur = remain.pop()  # cur = x-y
                    for dest, src, rng in _map:  # src-(src+rng-1) = a-b
                        if cur[1] < src or src + rng <= cur[0]:  # no overlap, x-y-a-b or a-b-x-y
                            continue
                        elif src <= cur[0] <= cur[1] < src + rng:  # a-x-y-b
                            offset = cur[0] - src
                            result.append((dest + offset, dest + offset + cur[1] - cur[0]))
                            break
                        elif cur[0] < src <= cur[1] < src + rng:  # x-a-y-b
                            offset = cur[1] - src
                            result.append((dest, dest + offset))
                            remain.append((cur[0], src - 1))
                            break
                        elif src <= cur[0] < src + rng <= cur[1]:  # a-x-b-y
                            offset = cur[0] - src
                            result.append((dest + offset, dest + rng - 1))
                            remain.append((src + rng, cur[1]))
                            break
                        elif cur[0] < src <= src + rng <= cur[1]:  # x-a-b-y
                            result.append((dest, dest + rng - 1))
                            remain.append((cur[0], src - 1))
                            remain.append((src + rng, cur[1]))
                            break
                    else:  # didn't match any source range
                        result.append(cur)
                remain = result
                result = []
            locations.extend(remain)

        # print(locations)
        return min(i[0] for i in locations)
