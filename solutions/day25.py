from utils.solution_base import SolutionBase
import networkx as nx
import math


class Solution(SolutionBase):
    def part1(self, data):
        g = nx.Graph()
        for line in data:
            name, cmps = line.split(": ")
            for cmp in cmps.split():
                g.add_edge(name, cmp)

        cuts = nx.minimum_edge_cut(g)
        g.remove_edges_from(cuts)
        groups = nx.connected_components(g)

        return math.prod(map(len, groups))

    def part2(self, data):
        return "HoHoHo"
