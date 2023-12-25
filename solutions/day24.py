from utils.solution_base import SolutionBase
from itertools import combinations
import z3


class Solution(SolutionBase):
    def part1(self, data):
        hails = []
        for line in data:
            pos, vel = line.split(" @ ")
            pos = tuple(map(int, pos.split(",")))
            vel = tuple(map(int, vel.split(",")))
            hails.append((pos, vel))

        formulas = {}
        for hail in hails:
            pos, vel = hail
            x, y, z = pos
            a, b, c = vel
            t = a / b
            u = x - t * y
            f = (1, -t, -u)
            formulas[hail] = f

        if len(data) == 5:
            _range = (7, 27)
        else:
            _range = (200000000000000, 400000000000000)

        r = 0
        groups = combinations(hails, 2)

        for group in groups:
            f1 = formulas[group[0]]
            f2 = formulas[group[1]]

            x1, y1, z1 = group[0][0]
            x2, y2, z2 = group[1][0]
            vel1 = group[0][1]
            vel2 = group[1][1]

            a1, b1, c1 = f1
            a2, b2, c2 = f2

            b = b2 - b1
            c = c2 - c1
            if b == 0:
                # print("parallel")
                continue
            else:
                y = -c / b
                x = (-b1 * y - c1) / a1

                if _range[0] <= x <= _range[1] and _range[0] <= y <= _range[1]:
                    sign1 = (1 if vel1[0] > 0 else -1, 1 if vel1[1] > 0 else -1)
                    sign2 = (1 if vel2[0] > 0 else -1, 1 if vel2[1] > 0 else -1)

                    test1 = (1 if x - x1 > 0 else -1, 1 if y - y1 > 0 else -1)
                    test2 = (1 if x - x2 > 0 else -1, 1 if y - y2 > 0 else -1)

                    if sign1 == test1 and sign2 == test2:
                        # print("match")
                        r += 1

        return r

    def part2(self, data):
        """
        refs:
        https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kepu26z/

        tried to find a solution without using third party libraries but failed
        use the z3 solver to solve the equations for now

        after solved the part 2 I found the refs above but still try to understand them
        may implement them later
        """
        hails = []
        for line in data:
            pos, vel = line.split(" @ ")
            pos = tuple(map(int, pos.split(",")))
            vel = tuple(map(int, vel.split(",")))
            hails.append((pos, vel))

        # using z3 to solve the system of equations
        px, py, pz, vx, vy, vz = z3.Ints("px py pz vx vy vz")
        times = [z3.Int("t" + str(i)) for i in range(len(hails))]

        s = z3.Solver()
        for i, (pos, vel) in enumerate(hails):
            s.add(px + vx * times[i] == pos[0] + vel[0] * times[i])
            s.add(py + vy * times[i] == pos[1] + vel[1] * times[i])
            s.add(pz + vz * times[i] == pos[2] + vel[2] * times[i])
        s.check()
        ans = s.model().evaluate(px + py + pz)

        return ans.as_long()
