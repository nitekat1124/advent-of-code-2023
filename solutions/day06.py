from utils.solution_base import SolutionBase
import math


class Solution(SolutionBase):
    def part1(self, data):
        _times = [*map(int, data[0].split(":")[1].strip().split())]
        _dists = [*map(int, data[1].split(":")[1].strip().split())]

        counts = []
        for i in range(len(_times)):
            _time = _times[i]
            _dist = _dists[i]
            counts.append(sum((t * (_time - t) > _dist) for t in range(_time)))

        return math.prod(counts)

    def part2(self, data):
        _time = int(data[0].split(":")[1].replace(" ", ""))
        _dist = int(data[1].split(":")[1].replace(" ", ""))

        """
        # approach 1, benchmark: 3.61 s
        # count every number in range 1 to _time
        count = sum((i * (_time - i)) > _dist for i in range(1, _time))
        """

        """
        # approach 2, benchmark: 1.84 s
        # act like approach but only count in half range
        mid = _time // 2
        times = 1 + _time % 2
        count = sum((i * (_time - i) > _dist) for i in range(mid - 1, 0, -1)) * 2
        count += (mid * (_time - mid) > _dist) * times
        """

        """
        # approach 3, benchmark: 1.05 s
        # look at the following patterns:
        #
        # even:
        # time = 8
        # 7 12 15 16 15 12 7
        #
        # time = 10
        # 9 16 21 24 25 24 21 16 9
        #
        # time = 12
        # 11 20 27 32 35 36 35 32 27 20 11
        #
        # odd:
        # time = 7
        # 6 10 12 12 10 6
        #
        # time = 9
        # 8 14 18 20 20 18 14 8
        #
        # time = 11
        # 10 18 24 28 30 30 28 24 18 10
        #
        # time = 13
        # 12 22 30 36 40 42 42 40 36 30 22 12
        #
        # so the rules are:
        # 1. find the highest number, which is floor((time/2)^2)
        # 2. if time is even, there will be only 1 highest number, and the decrease steps are 1, 3, 5, 7, 9, ...
        # 3. if time is odd, there will be 2 highest numbers, and the decrease steps are 2, 4, 6, 8, 10, ...
        """
        curr = _time**2 // 4  # the middle, is the highest record you can get
        step = 2 if _time % 2 else 1
        count = 0

        while curr > _dist:
            count += 1
            curr -= step
            step += 2
        count = count * 2 - (1 - _time % 2)  # there is only one middle number if _time is even

        return count
