from utils.solution_base import SolutionBase
from functools import reduce


class Solution(SolutionBase):
    def part1(self, data):
        data = data[0].split(",")
        return sum(self.calc_hash(item) for item in data)

    def part2(self, data):
        data = data[0].split(",")
        boxes = [{} for _ in range(256)]

        for line in data:
            if "=" in line:
                label, value = line.split("=")
                box_id = self.calc_hash(label)
                boxes[box_id][label] = int(value)
            else:
                label = line[:-1]
                box_id = self.calc_hash(label)
                if label in boxes[box_id]:
                    del boxes[box_id][label]

        power = 0
        for box_id1, box in enumerate(boxes, 1):
            for slot_id, lens in enumerate(box.items(), 1):
                power += box_id1 * slot_id * lens[1]

        return power

    def calc_hash(self, item):
        return reduce(lambda acc, c: (acc + ord(c)) * 17 % 256, item, 0)
