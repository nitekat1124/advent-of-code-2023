from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        start = (0, 0)
        d = 0
        return self.calc(data, start, d)

    def part2(self, data):
        h = len(data)
        w = len(data[0])
        results = []

        for y in range(h):
            for x in range(w):
                # check if it's on the edge
                if y not in [0, h - 1] and x not in [0, w - 1]:
                    continue

                init_d = []

                if y == 0:
                    init_d.append(1)
                elif y == h - 1:
                    init_d.append(3)

                if x == 0:
                    init_d.append(0)
                elif x == w - 1:
                    init_d.append(2)

                for d in init_d:
                    results.append(self.calc(data, (y, x), d))

        return max(results)

    def calc(self, data, start, init_d):
        # start = (0, 0)
        q = [(start, init_d)]  # (position, direction)
        visited = set()
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        h = len(data)
        w = len(data[0])

        while q:
            pos, d = q.pop(0)

            if (pos, d) in visited:
                continue
            visited.add((pos, d))

            _next_d = []
            curr = data[pos[0]][pos[1]]

            if curr == ".":
                _next_d.append(d)
            elif curr == "\\":
                # _next_d.append([1, 0, 3, 2][d])
                _next_d.append(d + (-1) ** d)
            elif curr == "/":
                # _next_d.append([3, 2, 1, 0][d])
                _next_d.append(3 - d)
            elif curr == "-":
                if d % 2:
                    _next_d.append((d + 1) % 4)
                    _next_d.append((d + 3) % 4)
                else:
                    _next_d.append(d)
            elif curr == "|":
                if d % 2:
                    _next_d.append(d)
                else:
                    _next_d.append((d + 1) % 4)
                    _next_d.append((d + 3) % 4)

            for _d in _next_d:
                y, x = (pos[0] + dirs[_d][0], pos[1] + dirs[_d][1])
                if 0 <= y < h and 0 <= x < w and ((y, x), _d) not in visited:
                    q.append(((y, x), _d))

        return len(set(pos for pos, _ in visited))
