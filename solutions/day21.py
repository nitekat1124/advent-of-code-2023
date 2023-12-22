from utils.solution_base import SolutionBase
from copy import deepcopy
from collections import deque


class Solution(SolutionBase):
    def part1(self, data):
        _map = []
        start = None
        for i, line in enumerate(data):
            _map.append(list(line))
            if "S" in line:
                start = (i, line.index("S"))

        history = [{start}]
        step = 0

        while step < 64:
            step += 1
            reach = set()

            for pos in history[-1]:
                y, x = pos
                for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < len(_map) and 0 <= nx < len(_map[0]) and _map[ny][nx] != "#":
                        reach.add((ny, nx))
            history.append(reach)

        return len(history[-1])

    def part2(self, data):
        """
        1. fix the map, remove the unreachable plots (it turns out that it's not necessary)
        2. find how many step to reach the edge center or corner from every
           starting point (center, edge center, corner)
        3. total steps is 26501365, which is 65 + 131 * 202300
           by (2), we found out the step from one edge to another edge is also 131
           that means there are 202300 extend maps in each direction for the original map
           forming a big diamond shape
        3. count the number of completely reached maps and the edge/corner map in that big diamond
        4. determine how many plot is reached in the completely reached map, considering whether the step count is odd or even
        5. determine how many plot is reached in the edge/corner map
        6. sum these up
        """
        _map = []
        start = None
        for i, line in enumerate(data):
            _map.append(list(line))
            if "S" in line:
                start = (i, line.index("S"))

        w = len(_map[0])
        h = len(_map)

        # fix the map, remove the unreachable plots
        # _map = self.fix_map(_map, start)

        edge_centers = [(0, w // 2), (h // 2, w - 1), (h - 1, w // 2), (h // 2, 0)]  # up, right, down, left
        corners = [(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)]  # up-left, up-right, down-right, down-left

        edge_starts = [(-1, w // 2), (h // 2, w), (h, w // 2), (h // 2, -1)]  # up, right, down, left
        corner_starts = [(-1, 0), (-1, w - 1), (h, w - 1), (h, 0)]  # up-left, up-right, down-right, down-left

        starts = [start] + edge_starts + corner_starts
        targets = edge_centers + corners

        _ = self.find_steps(_map, starts, targets)
        # print(*sorted(step_data.items()), sep="\n")

        # print([i for i in self.cache.items() if i[0][0] == start][:10])

        n = 26501365
        p = (n - w // 2) // w
        # print(p)

        reaches = [0, 0]
        reaches[1] = len([i for i in self.cache.items() if i[0][0] == start and i[1] % 2])
        reaches[0] = len([i for i in self.cache.items() if i[0][0] == start and i[1] % 2 == 0])
        # print(c)

        # a1 = self.checklen(_map, (130, 130), 196, 1)
        # b1 = self.checklen(_map, (130, 0), 196, 1)
        # c1 = self.checklen(_map, (0, 0), 196, 1)
        # d1 = self.checklen(_map, (0, 130), 196, 1)
        a1 = len([i for i in self.cache.items() if i[0][0] == (131, 130) and i[1] <= 196 + 1 and i[1] % 2])
        b1 = len([i for i in self.cache.items() if i[0][0] == (131, 0) and i[1] <= 196 + 1 and i[1] % 2])
        c1 = len([i for i in self.cache.items() if i[0][0] == (-1, 0) and i[1] <= 196 + 1 and i[1] % 2])
        d1 = len([i for i in self.cache.items() if i[0][0] == (-1, 130) and i[1] <= 196 + 1 and i[1] % 2])
        # print(a1, b1, c1, d1)

        # a2 = self.checklen(_map, (131, 130), 66, 1)
        # b2 = self.checklen(_map, (131, 0), 66, 1)
        # c2 = self.checklen(_map, (-1, 0), 66, 1)
        # d2 = self.checklen(_map, (-1, 130), 66, 1)
        a2 = len([i for i in self.cache.items() if i[0][0] == (131, 130) and i[1] <= 66 and i[1] % 2 == 0])
        b2 = len([i for i in self.cache.items() if i[0][0] == (131, 0) and i[1] <= 66 and i[1] % 2 == 0])
        c2 = len([i for i in self.cache.items() if i[0][0] == (-1, 0) and i[1] <= 66 and i[1] % 2 == 0])
        d2 = len([i for i in self.cache.items() if i[0][0] == (-1, 130) and i[1] <= 66 and i[1] % 2 == 0])
        # print(a2, b2, c2, d2)

        tmp = p - 1
        s = 1
        r = 0
        while tmp > 0:
            rr = 0
            rr += reaches[s] * (tmp // 2)
            rr += reaches[1 - s] * (tmp - (tmp // 2))
            rr *= 2
            rr += reaches[s]

            r += rr
            if tmp < p - 1:
                r += rr

            # mm = 2 if tmp == 1 else 1

            # r += a1 + b1 + c1 + d1
            # r += (a2 + b2 + c2 + d2) * mm

            tmp -= 1
            s = 1 - s

        r += (a1 + b1 + c1 + d1) * (p - 1)
        r += (a2 + b2 + c2 + d2) * p

        tt = len([i for i in self.cache.items() if i[0][0] == (131, 65) and i[1] <= 131 and i[1] % 2])
        gg = len([i for i in self.cache.items() if i[0][0] == (65, -1) and i[1] <= 131 and i[1] % 2])
        bb = len([i for i in self.cache.items() if i[0][0] == (-1, 65) and i[1] <= 131 and i[1] % 2])
        ll = len([i for i in self.cache.items() if i[0][0] == (65, 131) and i[1] <= 131 and i[1] % 2])
        # print(tt, gg, bb, ll)

        r += tt + gg + bb + ll
        r += reaches[0] * 2

        return r

    def fix_map(self, _map, start):
        w = len(_map[0])
        h = len(_map)

        plots = set()
        for y in range(h):
            for x in range(w):
                if _map[y][x] == ".":
                    plots.add((y, x))

        visited = set(start)
        q = deque([start])

        while q:
            y, x = q.popleft()

            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and (ny, nx) not in visited and (ny, nx) in plots:
                    q.append((ny, nx))
                    visited.add((ny, nx))

        unreachable = plots - visited
        _map_fix = deepcopy(_map)
        for y, x in unreachable:
            _map_fix[y][x] = "#"
        return _map_fix

    def find_steps(self, _map, starts, targets):
        """
        find how many steps to reach the target from every start
        """
        w = len(_map[0])
        h = len(_map)

        self.cache = {}  # key: (search_start, any point), value: steps
        step_data = {}  # key: (search_start, search_target), value: steps

        for start in starts:
            q = deque([start])
            visited = set()
            # steps = 0
            steps = 1 - (65 in start)

            while q:
                steps += 1

                for _ in range(len(q)):
                    y, x = q.popleft()

                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and (ny, nx) not in visited and _map[ny][nx] != "#":
                            q.append((ny, nx))
                            visited.add((ny, nx))
                            self.cache[(start, (ny, nx))] = steps  # + [1, 0][start == (h // 2, w // 2)]

                for target in targets:
                    if target == start:
                        continue
                    if target in visited and (start, target) not in step_data and sum(abs(a - b) for a, b in zip(start, target)) != 1:
                        step_data[(start, target)] = steps
        return step_data

    def checklen(self, _map, start, step_max, step_init=0):
        w = len(_map[0])
        h = len(_map)

        q = deque([start])
        steps = step_init

        while steps < step_max:
            steps += 1
            q2 = set()

            for _ in range(len(q)):
                y, x = q.popleft()

                for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and _map[ny][nx] != "#":
                        q2.add((ny, nx))

            q = deque(list(q2))

        return len(q)
