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
        """
        benchmarks:
        part2_original:     661.71 µs
        part2_overlap_alt:  1.03 ms
        part2_reverse:      161.51 s

        notes:
        part2_original is my initial solution to this puzzle, it checks whether the current range
        overlaps with any map (there are four possible overlaps). if there is an overlap, the
        non-overlapping part will be put back into the remaining list to be checked for further
        examination later.

        part2_overlap_alt uses a different method to check and cut overlapping/non-overlapping
        ranges, which looks easier to read but runs slower. overall I think it's not much different
        from the part2_original.

        part2_reverse reverses the entire map, then starts from location 0 to check the value of
        seed and checks if it is in the range of seeds. I think this approach is very easy to
        understand, but runs way tooooooooo slow.
        """

        return self.part2_original(data)
        # return self.part2_overlap_alt(data)
        # return self.part2_reverse(data)

    def part2_original(self, data):
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

    def part2_overlap_alt(self, data):
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
                        else:
                            # calculate the overlap and left/right outside the overlap
                            # maybe easier to understand, but runs slower
                            outside_left = (min(cur[0], src), min(cur[1], src) - 1)
                            if outside_left[0] <= outside_left[1]:
                                remain.append(outside_left)

                            outside_right = (max(cur[0], src + rng), max(cur[1], src + rng) - 1)
                            if outside_right[0] <= outside_right[1]:
                                remain.append(outside_right)

                            overlap = (max(cur[0], src), min(cur[1], src + rng - 1))
                            if overlap[0] <= overlap[1]:
                                offset = overlap[0] - src
                                result.append((dest + offset, dest + offset + overlap[1] - overlap[0]))

                            break
                    else:  # didn't match any source range
                        result.append(cur)
                remain = result
                result = []
            locations.extend(remain)

        # print(locations)
        return min(i[0] for i in locations)

    def part2_reverse(self, data):
        seeds = [*map(int, data[0].split(": ")[1].split())]
        maps = [[[*map(int, n.split())] for n in i.split("\n")[1:]] for i in "\n".join(data[2:]).split("\n\n")]

        location = 0
        seed_pairs = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]

        while True:
            result = location
            for _map in maps[::-1]:
                for dest, src, rng in _map:
                    if dest <= result < dest + rng:
                        idx = result - dest
                        result = src + idx
                        break
            if any(pair[0] <= result <= pair[1] for pair in seed_pairs):
                return location
            location += 1
