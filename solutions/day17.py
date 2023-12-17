from utils.solution_base import SolutionBase
from heapq import heappop, heappush


class Solution(SolutionBase):
    def part1(self, data):
        return self.find_path(data, 1, 3)

    def part2(self, data):
        return self.find_path(data, 4, 10)

    def find_path(self, data, minimum_step_before_turn=1, maximum_consecutive_steps=3):
        h = len(data)
        w = len(data[0])
        start = (0, 0)
        end = (h - 1, w - 1)

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        visited = {}  # {(pos, d): loss}
        q = [(0, start, -1, 0)]  # (loss, pos, dir, dir_continious)
        # losses = []
        """
        Since I switched to using heapq, there's no need to store every loss.
        However, I've kept it as a comment in the code as a reminder(?) of how I came up with the solution.
        """

        while q:
            loss, pos, d, dc = heappop(q)
            if pos == end:
                return loss
                # losses.append(loss)
                # continue

            """
            find allowed directions:

            already listed all possible steps in the current direction before,
            so there's no need to repeat them (in the same direction)
            just added all possible steps to the left or right of the current position
            """
            allowed_dirs = [_d for _d in range(4) if _d != d and (_d + 2) % 4 != d]

            for _d in allowed_dirs:
                _next_loss = loss
                for d_cont in range(1, maximum_consecutive_steps + 1):
                    _next_pos = tuple(a + b * d_cont for a, b in zip(pos, dirs[_d]))
                    if 0 <= _next_pos[0] < h and 0 <= _next_pos[1] < w:
                        _next_loss += int(data[_next_pos[0]][_next_pos[1]])
                        if _next_loss < visited.get((_next_pos, _d), float("inf")):
                            visited[(_next_pos, _d)] = _next_loss
                            if d_cont >= minimum_step_before_turn:
                                heappush(q, (_next_loss, _next_pos, _d, d_cont))

        # return min(losses)
