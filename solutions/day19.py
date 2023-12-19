from utils.solution_base import SolutionBase
import math


class Solution(SolutionBase):
    def part1(self, data):
        sep = data.index("")
        _temp_flows = data[:sep]
        _temp_parts = data[sep + 1 :]

        flows = {}
        for flow in _temp_flows:
            name, rest = flow.split("{")
            rule = rest[:-1].split(",")
            flows[name] = rule

        parts = []
        for part in _temp_parts:
            cates = part[1:-1].split(",")
            part = {}
            for cate in cates:
                k, v = cate.split("=")
                part[k] = int(v)
            parts.append(part)

        ratings = 0
        for part in parts:
            curr = "in"
            while 1:
                ret = self.apply_rules(flows[curr], part)
                if ret == "R":
                    break
                elif ret == "A":
                    ratings += sum(part.values())
                    break
                else:
                    curr = ret

        return ratings

    def apply_rules(self, rules, part):
        for rule in rules:
            if ":" in rule:
                condition, _next = rule.split(":")
                cate, value = condition[0], int(condition[2:])
                if condition[1] == "<":
                    if part[cate] < value:
                        return _next
                else:  # condition[1] == ">"
                    if part[cate] > value:
                        return _next
            else:
                return rule

    def part2(self, data):
        sep = data.index("")
        _temp_flows = data[:sep]

        flows = {}
        for flow in _temp_flows:
            name, rest = flow.split("{")
            rule = rest[:-1].split(",")
            flows[name] = rule

        parts = {
            "x": {(1, 4000)},
            "m": {(1, 4000)},
            "a": {(1, 4000)},
            "s": {(1, 4000)},
        }

        n = 0
        q = [(parts, "in")]

        while q:
            parts, curr = q.pop(0)
            rets = self.apply_rules2(flows[curr], parts)

            for ret in rets:
                if ret["next"] == "R":
                    continue
                elif ret["next"] == "A":
                    n += math.prod(_range[1] - _range[0] + 1 for _ranges in ret["parts"].values() for _range in _ranges)
                else:
                    q.append((ret["parts"], ret["next"]))

        return n

    def apply_rules2(self, rules, parts):
        rets = []

        for rule in rules:
            if ":" in rule:
                condition, _next = rule.split(":")
                cate, value = condition[0], int(condition[2:])
                need_del = set()
                need_add = set()
                if condition[1] == "<":
                    for item in parts[cate]:
                        if item[1] < value:
                            """
                            use union on dict
                            thanks to asavar https://www.reddit.com/r/adventofcode/comments/18ltr8m/comment/ke1isb7/
                            """
                            rets.append({"next": _next, "parts": parts | {cate: {item}}})
                            need_del.add(item)
                        if item[0] < value <= item[1]:
                            rets.append({"next": _next, "parts": parts | {cate: {(item[0], value - 1)}}})
                            need_del.add(item)
                            need_add.add((value, item[1]))
                else:  # condition[1] == ">"
                    for item in parts[cate]:
                        if item[0] > value:
                            rets.append({"next": _next, "parts": parts | {cate: {item}}})
                            need_del.add(item)
                        if item[1] > value >= item[0]:
                            rets.append({"next": _next, "parts": parts | {cate: {(value + 1, item[1])}}})
                            need_del.add(item)
                            need_add.add((item[0], value))
                parts[cate] = parts[cate] - need_del | need_add
            else:
                rets.append({"next": rule, "parts": parts})

        return rets
