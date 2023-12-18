from utils.solution_base import SolutionBase
import re

"""
F - 7
|   |
L - J
"""


class Solution(SolutionBase):
    def part1(self, data):
        _map, _start, _loop_nodes = self.parse_map(data)
        return len(_loop_nodes) // 2

    def part2(self, data):
        _map, _start, _loop_nodes = self.parse_map(data)
        row_counts = []

        for h, items in enumerate(_map):
            line = [v if (h, w) in _loop_nodes else "." for w, v in enumerate(items)]
            line = "".join(line)

            line = re.sub(r"L-*7", "|", line)
            line = re.sub(r"L-*J", "||", line)
            line = re.sub(r"F-*7", "||", line)
            line = re.sub(r"F-*J", "|", line)

            cross = 0
            inside = 0

            for c in line:
                if c == "." and cross % 2:
                    inside += 1
                elif c in "F7LJ|":
                    cross += 1
            row_counts.append(inside)
        return sum(row_counts)

    def part2_shoelace_picks(self, data):
        # region same as self.parse_map()
        _start = None
        _map = []

        for h, line in enumerate(data):
            _map.append(list(line))
            if "S" in line:
                _start = (h, line.index("S"))

        """ four adjacent directions """
        adj_dirs = [  # top, right, bottom, left
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ]

        """ define the direction connected to the adjacent node for each symbol """
        symbol_connects = {  # top, right, bottom, left
            "|": (1, 0, 1, 0),
            "-": (0, 1, 0, 1),
            "L": (1, 1, 0, 0),
            "J": (1, 0, 0, 1),
            "7": (0, 0, 1, 1),
            "F": (0, 1, 1, 0),
        }

        """ define the types of adjacent nodes that can be connected for each direction """
        # adj_connect_types = {pos: [k for k, v in symbol_connects.items() if v[(i + 2) % 4]] for i, pos in enumerate(adj_dirs)}
        adj_connect_types = {
            (-1, 0): "F|7",
            (0, 1): "7-J",
            (1, 0): "L|J",
            (0, -1): "F-L",
        }

        adjs = [0, 0, 0, 0]  # top, right, bottom, left
        for i, adj in enumerate(adj_dirs):
            pos = tuple(a + b for a, b in zip(_start, adj))
            if _map[pos[0]][pos[1]] in adj_connect_types[adj]:
                adjs[i] = 1

        _map[_start[0]][_start[1]] = {v: k for k, v in symbol_connects.items()}[tuple(adjs)]
        # endregion

        # order the corner nodes
        nodes_ordered = []
        visited = set()
        curr = _start
        while curr not in visited:
            visited.add(curr)
            c = _map[curr[0]][curr[1]]
            if c in "LJ7F":
                nodes_ordered.append(curr)
            ds = [adj_dirs[i] for i, v in enumerate(symbol_connects[c]) if v == 1]
            _next = tuple(map(sum, zip(curr, ds[0])))
            if _next in visited:
                _next = tuple(map(sum, zip(curr, ds[1])))
            curr = _next
        nodes_ordered.append(_start)

        # shoelace formula
        area = 0
        for i in range(len(nodes_ordered) - 1):
            y1, x1 = nodes_ordered[i]
            y2, x2 = nodes_ordered[i + 1]
            area += x1 * y2 - x2 * y1
        area = abs(area) // 2

        # pick's theorem
        internal = area - len(visited) // 2 + 1
        return internal

    def parse_map(self, data):
        start = None
        _map = []

        for h, line in enumerate(data):
            _map.append(list(line))
            if "S" in line:
                start = (h, line.index("S"))

        """ four adjacent directions """
        adj_dirs = [  # top, right, bottom, left
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ]

        """ define the direction connected to the adjacent node for each symbol """
        symbol_connects = {  # top, right, bottom, left
            "|": (1, 0, 1, 0),
            "-": (0, 1, 0, 1),
            "L": (1, 1, 0, 0),
            "J": (1, 0, 0, 1),
            "7": (0, 0, 1, 1),
            "F": (0, 1, 1, 0),
        }

        """ define the types of adjacent nodes that can be connected for each direction """
        # adj_connect_types = {pos: [k for k, v in symbol_connects.items() if v[(i + 2) % 4]] for i, pos in enumerate(adj_dirs)}
        adj_connect_types = {
            (-1, 0): "F|7",
            (0, 1): "7-J",
            (1, 0): "L|J",
            (0, -1): "F-L",
        }

        adjs = [0, 0, 0, 0]  # top, right, bottom, left
        for i, adj in enumerate(adj_dirs):
            pos = tuple(a + b for a, b in zip(start, adj))
            if _map[pos[0]][pos[1]] in adj_connect_types[adj]:
                adjs[i] = 1

        _map[start[0]][start[1]] = {v: k for k, v in symbol_connects.items()}[tuple(adjs)]

        queue = [start]
        visited = set()

        while queue:
            pos = queue.pop(0)
            if pos in visited:
                continue
            visited.add(pos)
            if _map[pos[0]][pos[1]] in " .":
                continue

            sym = _map[pos[0]][pos[1]]
            _dirs = [adj_dirs[i] for i, v in enumerate(symbol_connects[sym]) if v == 1]
            for dy, dx in _dirs:
                queue.append((pos[0] + dy, pos[1] + dx))

        return _map, start, visited
