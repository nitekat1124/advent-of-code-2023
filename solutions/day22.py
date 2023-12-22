from utils.solution_base import SolutionBase
from collections import defaultdict
from itertools import product
from copy import deepcopy  # noqa: F401, used in the old solution


class Solution(SolutionBase):
    def parse_data(self, data):
        space = {}
        bricks = defaultdict(list)

        for i, line in enumerate(data, 1):
            _from, _to = map(lambda x: [*map(int, x.split(","))], line.split("~"))
            x_range, y_range, z_range = [range(_f, _t + 1) for _f, _t in zip(_from, _to)]
            positions = [*product(x_range, y_range, z_range)]
            for pos in positions:
                space[pos] = i
                bricks[i].append(pos)

        return space, bricks

    def fall(self, space, bricks):
        max_z = max(z for x, y, z in space)

        # start from z = 2
        h = 2

        while h <= max_z:
            found_bricks = set([v for k, v in space.items() if k[2] == h])
            fall = False
            for bid in found_bricks:
                _brick = bricks[bid]
                low_z = min(z for x, y, z in _brick)

                # if this brick has a lower point than current height, skip
                if low_z < h:
                    continue

                safe = False
                # find all the coords that has z = current height
                pos_need_check = [i for i in _brick if i[2] == h]
                for x, y, z in pos_need_check:
                    # if there is a brick under this brick, safe
                    if (x, y, z - 1) in space:
                        safe = True
                        break
                if not safe:
                    # fall, update all the coords of this brick
                    bricks[bid] = []
                    for x, y, z in _brick:
                        space[(x, y, z - 1)] = bid
                        del space[(x, y, z)]
                        bricks[bid].append((x, y, z - 1))
                    fall = True

            if h == 2:
                h += 1
            else:
                if fall:
                    h -= 1
                else:
                    h += 1

        return space, bricks

    def check_placements(self, space, bricks):
        placements = {}
        for bid in bricks:
            _brick = bricks[bid]
            low_z = min(z for x, y, z in _brick)
            if low_z > 1:
                need_check = [pos for pos in _brick if pos[2] == low_z]
                place = set()
                for x, y, z in need_check:
                    if (x, y, z - 1) in space:
                        place.add(space[(x, y, z - 1)])
                placements[bid] = place
        self.placements = placements

    def count_possible_fallen(self, bid):
        fallen = set([bid])
        upper_falls = 1

        while upper_falls:
            upper_falls = 0
            for p_id in self.placements:
                if p_id not in fallen and all(placed_on in fallen for placed_on in self.placements[p_id]):
                    fallen.add(p_id)
                    upper_falls += 1

        return len(fallen) - 1

    def part1(self, data):
        space, bricks = self.parse_data(data)
        space, bricks = self.fall(space, bricks)
        self.check_placements(space, bricks)

        count = 0
        # initial solution, it could run but it's slow
        """
        for bid in bricks:
            space_copy = deepcopy(space)
            for x, y, z in bricks[bid]:
                del space_copy[(x, y, z)]

            high_z = max(z for x, y, z in bricks[bid])

            # find the coords that current brick has on z = high_z
            cbhz = [pos for pos in bricks[bid] if pos[2] == high_z]

            # every coord in cbhz with z + 1 are needed to check if there is a brick at that position
            need_check = [(x, y, z + 1) for x, y, z in cbhz]

            # find the bricks id that in the need_check
            need_check_bid = set([_bid for _pos, _bid in space_copy.items() if _pos in need_check])

            # no other brick place on it, safe
            if len(need_check_bid) == 0:
                count += 1
                continue

            fall_count = 0
            for ncb_id in need_check_bid:
                ncb = bricks[ncb_id]
                low_z = min(z for x, y, z in ncb)

                safe = False
                # check if there is another brick under this brick
                for x, y, z in [_pos for _pos in ncb if _pos[2] == low_z]:
                    if (x, y, z - 1) in space_copy:
                        safe = True
                        break
                if not safe:
                    fall_count += 1

            # if no brick fall, safe
            if fall_count == 0:
                count += 1
        """

        for bid in bricks:
            # find which brick placed on it
            placed_on_it = [k for k, v in self.placements.items() if bid in v]

            # if no brick placed on it, safe
            if len(placed_on_it) == 0:
                count += 1
                continue

            fall_count = 0
            for p_id in placed_on_it:
                placed_on = self.placements[p_id]
                # if placed on more than one brick, save
                if len(placed_on) == 1:
                    fall_count += 1

            # if no brick fall, safe
            if fall_count == 0:
                count += 1

        return count

    def part2(self, data):
        space, bricks = self.parse_data(data)
        space, bricks = self.fall(space, bricks)
        self.check_placements(space, bricks)

        count = 0
        # initial solution, it could run but it's slow
        """
        for bid in bricks:
            space_copy = deepcopy(space)
            for x, y, z in bricks[bid]:
                del space_copy[(x, y, z)]

            high_z = max(z for x, y, z in bricks[bid])

            # find the coords that current brick has on z = high_z
            cbhz = [pos for pos in bricks[bid] if pos[2] == high_z]

            need_check = [(x, y, z + 1) for x, y, z in cbhz]

            need_check_bid = set([_bid for _pos, _bid in space_copy.items() if _pos in need_check])

            # no other brick place on it, safe
            if len(need_check_bid) == 0:
                continue

            fall_count = 0
            for ncb_id in need_check_bid:
                ncb = bricks[ncb_id]
                low_z = min(z for x, y, z in ncb)

                safe = False
                for x, y, z in [_pos for _pos in ncb if _pos[2] == low_z]:
                    if (x, y, z - 1) in space_copy:
                        safe = True
                        break
                if not safe:
                    fall_count += 1

            if fall_count:
                count += self.count_possible_fallen(bid)
        """

        for bid in bricks:
            # find which brick placed on it
            placed_on_it = [k for k, v in self.placements.items() if bid in v]

            # if no brick placed on it, safe
            if len(placed_on_it) == 0:
                continue

            fall_count = 0
            for p_id in placed_on_it:
                placed_on = self.placements[p_id]
                # if placed on more than one brick, save
                if len(placed_on) == 1:
                    fall_count += 1

            # if there is a brick fall, count the number of bricks that fall
            if fall_count:
                count += self.count_possible_fallen(bid)

        return count
