from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        # return self.part1_org(data)
        curr = (0, 0)
        dirs = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
        }
        points = [curr]
        edges = 0

        for line in data:
            d, _l, c = line.split()
            edges += int(_l)
            end = tuple(a + int(_l) * b for a, b in zip(curr, dirs[d]))
            points.append(end)
            curr = end

        return self.calc_area(points, edges)

    def part2(self, data):
        curr = (0, 0)
        dirs = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
        }
        points = [curr]

        edges = 0

        for line in data:
            d, _l, c = line.split()
            d = "RDLU"[int(c[-2])]
            _l = int(c[2:-2], 16)
            edges += _l
            end = tuple(a + _l * b for a, b in zip(curr, dirs[d]))
            points.append(end)
            curr = end

        return self.calc_area(points, edges)

    def calc_area(self, points, edges):
        """
        Thanks and learnt from the references:

        https://www.reddit.com/r/adventofcode/comments/18l2nk2/2023_day_18_easiest_way_to_solve_both_parts/
        https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kdv3pvu/

        https://en.wikipedia.org/wiki/Shoelace_formula
        https://en.wikipedia.org/wiki/Pick%27s_theorem
        """
        r = 0
        for i in range(len(points) - 1):
            y1, x1 = points[i]
            y2, x2 = points[i + 1]
            r += x1 * y2 - x2 * y1

        return abs(r) // 2 + edges // 2 + 1

    def part1_org(self, data):
        curr = (0, 0)
        dirs = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
        }
        dig = [curr]
        for line in data:
            d, _l, c = line.split()
            for i in range(int(_l)):
                curr = tuple(map(sum, zip(curr, dirs[d])))
                dig.append(curr)

        min_y = min(dig, key=lambda x: x[0])[0]
        max_y = max(dig, key=lambda x: x[0])[0]
        min_x = min(dig, key=lambda x: x[1])[1]
        max_x = max(dig, key=lambda x: x[1])[1]

        fills = 0

        for i in range(min_y, max_y + 1):
            x = 0
            for j in range(min_x, max_x + 1):
                if (i, j) in dig:
                    if (i - 1, j) in dig and (i + 1, j) in dig:
                        x += 1
                    else:
                        if (i + 1, j) in dig and (i, j + 1) in dig:  # F
                            s = 0
                            x += 1
                        elif (i - 1, j) in dig and (i, j + 1) in dig:  # L
                            s = 1
                            x += 1
                        else:
                            if (i + 1, j) in dig and (i, j - 1) in dig:  # 7
                                if s == 0:
                                    x += 1
                                s = 0
                            elif (i - 1, j) in dig and (i, j - 1) in dig:  # J
                                if s == 1:
                                    x += 1
                                s = 0
                else:
                    if x % 2:
                        fills += 1

        return len(set(dig)) + fills
