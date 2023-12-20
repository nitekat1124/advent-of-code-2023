from utils.solution_base import SolutionBase
import math


class Solution(SolutionBase):
    def part1(self, data):
        cycle = 0
        pulse_count = [0, 0]  # index: 0 = low, 1 = high

        mods = self.parse_modules(data)

        while cycle < 1000:
            cycle += 1
            """
            button to broadcaster add 1 low pulse
            broadcaster to its destinations add 1 low pulse each
            """
            pulse_count[0] += len(mods["broadcaster"]["dest"]) + 1

            q = [(mods["broadcaster"]["dest"], 0, "broadcaster")]  # destinations, pulse, source
            while q:
                dests, pulse, source = q.pop(0)
                for dest in dests:
                    if dest not in mods:  # already reached the untyped module (like output), do nothing
                        continue

                    if mods[dest]["type"] == "%":
                        if pulse == 0:  # only work on receive a low pulse
                            mods[dest]["switch"] = not mods[dest]["switch"]
                            _next_pulse = int(mods[dest]["switch"])
                            pulse_count[_next_pulse] += len(mods[dest]["dest"])
                            q.append((mods[dest]["dest"], _next_pulse, dest))
                    elif mods[dest]["type"] == "&":
                        mods[dest]["inputs"][source] = pulse
                        _next_pulse = 1 - all(mods[dest]["inputs"].values())
                        pulse_count[_next_pulse] += len(mods[dest]["dest"])
                        q.append((mods[dest]["dest"], _next_pulse, dest))

            if self.is_all_off(mods):
                break

        return ((1000 // cycle) ** 2) * math.prod(pulse_count)

    def parse_modules(self, data):
        mods = {}
        conj = {}

        for line in data:
            name, dest = line.split(" -> ")
            dest = set(dest.split(", "))

            mod = {"dest": dest}
            _type = name[0]

            if _type == "%":  # Flip-flop modules
                name = name[1:]
                mod["switch"] = False
            elif _type == "&":  # Conjunction modules
                name = name[1:]
                if name not in conj:
                    conj[name] = {}
                mod["inputs"] = conj[name]
            else:
                _type = name
            mod["type"] = _type
            mods[name] = mod

        for c in conj:
            for m in mods:
                if c in mods[m]["dest"]:
                    conj[c][m] = False

        return mods

    def is_all_off(self, mods):
        switch = {m: v["switch"] for m, v in mods.items() if v["type"] == "%"}
        if any(switch.values()):
            return False
        """
        in fact the requirement is only ask all flip-flop modules should be off
        no need to check conjunction modules
        """
        # inputs = {m: v["inputs"] for m, v in mods.items() if v["type"] == "&"}
        # if any(any(inputs[c].values()) for c in inputs):
        #     return False

        return True

    def part2(self, data):
        cycle = 0
        pulse_count = [0, 0]  # index: 0 = low, 1 = high

        mods = self.parse_modules(data)

        """
        from rx traversal back to it's parents, until reach a multi-input conjunction module
        find the cycles of the inputs of that conjunction module, calc the lcm of them
        """
        parents = set([m for m, v in mods.items() if "rx" in v["dest"]])
        expect_pulse = 0

        while 1:
            upper_parents = set([m for m, v in mods.items() if v["dest"] & parents])
            parents = upper_parents
            expect_pulse = 1 - expect_pulse
            if len(parents) > 1:
                break

        cycles = {mod: 0 for mod in parents}

        while 1:
            cycle += 1
            """
            button to broadcaster add 1 low pulse
            broadcaster to its destinations add 1 low pulse each
            """
            pulse_count[0] += len(mods["broadcaster"]["dest"]) + 1

            q = [(mods["broadcaster"]["dest"], 0, "broadcaster")]  # destinations, pulse, source
            while q:
                dests, pulse, source = q.pop(0)
                for dest in dests:
                    if dest not in mods:  # already reached the untyped module (like output), do nothing
                        continue

                    if mods[dest]["type"] == "%":
                        if pulse == 0:  # only work on receive a low pulse
                            mods[dest]["switch"] = not mods[dest]["switch"]
                            _next_pulse = int(mods[dest]["switch"])
                            pulse_count[_next_pulse] += len(mods[dest]["dest"])
                            q.append((mods[dest]["dest"], _next_pulse, dest))
                    elif mods[dest]["type"] == "&":
                        mods[dest]["inputs"][source] = pulse
                        _next_pulse = 1 - all(mods[dest]["inputs"].values())
                        pulse_count[_next_pulse] += len(mods[dest]["dest"])
                        q.append((mods[dest]["dest"], _next_pulse, dest))

                    if dest in cycles and cycles[dest] == 0 and _next_pulse == expect_pulse:
                        cycles[dest] = cycle

                    if all(cycles.values()):
                        return math.lcm(*cycles.values())
