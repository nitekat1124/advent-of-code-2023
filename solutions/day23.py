from utils.solution_base import SolutionBase
from collections import defaultdict, deque
import re


class Solution(SolutionBase):
    def part1(self, data):
        s = (0, data[0].index("."))
        e = (len(data) - 1, data[-1].index("."))

        dists = defaultdict(int)

        q = deque([(s, set())])
        res = []
        available = [
            ((0, 1), ">"),
            ((0, -1), "<"),
            ((1, 0), "v"),
            ((-1, 0), "^"),
        ]
        while q:
            pos, visited = q.popleft()
            if pos in visited:
                continue
            visited.add(pos)

            if pos in dists:
                if len(visited) < dists[pos]:
                    continue
                else:
                    dists[pos] = len(visited)

            r, c = pos
            if pos == e:
                res.append(len(visited) - 1)

            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc

                if 0 <= nr < len(data) and 0 <= nc < len(data[0]) and (data[nr][nc] == "." or ((dr, dc), data[nr][nc]) in available):
                    if (nr, nc) not in visited:
                        q.append(((nr, nc), visited | {pos}))

        return max(res)

    def part2_wtf(self, data):
        new_data = []
        for line in data:
            line = line.replace("^", ".")
            line = line.replace(">", ".")
            line = line.replace("v", ".")
            line = line.replace("<", ".")
            new_data.append(line)
        return self.part1(new_data)

    def part2(self, data):
        """
        1. find all intersections
        2. find all the connected path for each node (intersection, start, end)
        3. dfs using above infos
        """

        _map = []
        for line in data:
            line = re.sub(r"[\^>v<]", ".", line)
            _map.append(list(line))

        h = len(_map)
        w = len(_map[0])
        start = (0, data[0].index("."))
        end = (h - 1, data[-1].index("."))
        nodes = {start, end}

        # find all intersections
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if _map[y][x] == ".":
                    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    neighbors = [(y + d[0], x + d[1]) for d in dirs]
                    if sum(1 for ny, nx in neighbors if _map[ny][nx] == ".") > 2:
                        nodes.add((y, x))

        # find all the connected path for each node
        paths = {}
        connects = defaultdict(set)

        for node in nodes:
            q = deque([(node, set())])
            while q:
                pos, visited = q.popleft()
                if pos in visited:
                    continue
                visited.add(pos)
                r, c = pos
                for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w and _map[nr][nc] == "." and (nr, nc) not in visited:
                        if (nr, nc) in nodes:
                            paths[(node, (nr, nc))] = len(visited)
                            paths[((nr, nc), node)] = len(visited)
                            connects[node].add((nr, nc))
                            connects[(nr, nc)].add(node)
                        else:
                            q.append(((nr, nc), visited | {pos}))

        # find all possible routes
        q = deque([(start, [])])
        res = []
        while q:
            pos, history = q.pop()

            if pos == end:
                res.append(history + [pos])
                continue

            for node in connects[pos]:
                if node not in history and (pos, node) in paths:
                    q.append((node, history + [pos]))

        max_dist = 0
        for r in res:
            dist = 0
            for i in range(len(r) - 1):
                dist += paths[(r[i], r[i + 1])]
            max_dist = max(max_dist, dist)

        return max_dist
