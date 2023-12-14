from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        self._map = [list(line) for line in data]
        self.tilt()
        return self.count_total_load()

    def part2(self, data):
        self._map = [list(line) for line in data]

        cycle = 1000000000
        cache = {}

        for cycle_idx in range(cycle):
            for _ in range(4):
                self.tilt()
                self.turn()

            _hash = hash("".join("".join(x) for x in self._map))

            if _hash not in cache:
                cache[_hash] = cycle_idx
            else:
                diff = cycle_idx - cache[_hash]
                head = cache[_hash]
                rest = cycle - ((cycle - head) // diff) * diff - head - 1
                break

        for _ in range(rest):
            for _ in range(4):
                self.tilt()
                self.turn()

        return self.count_total_load()

    def tilt(self):
        for i in range(1, len(self._map)):
            for x, c in enumerate(self._map[i]):
                if c == "O":
                    col = [row[x] for row in self._map]
                    prev_y = i
                    for y in range(i - 1, -1, -1):
                        if col[y] == ".":
                            self._map[y][x] = "O"
                            self._map[prev_y][x] = "."
                            prev_y = y
                        elif col[y] == "#":
                            break

    def turn(self):
        self._map = [list(x)[::-1] for x in zip(*self._map)]

    def count_total_load(self):
        height = len(self._map)
        return sum((height - i) * sum(1 for c in line if c == "O") for i, line in enumerate(self._map))
