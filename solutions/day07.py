from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        hands = [line.split() for line in data]
        hands = [(self.label_to_number(hand[0]), int(hand[1]), self.get_score(hand[0])) for hand in hands]
        hands = sorted(hands, key=lambda hand: (hand[2], hand[0]))
        return sum(rank * hand[1] for rank, hand in enumerate(hands, 1))

    def part2(self, data):
        hands = [line.split() for line in data]
        hands = [(self.label_to_number(hand[0], wildcard=True), int(hand[1]), self.get_score(hand[0], wildcard=True)) for hand in hands]
        hands = sorted(hands, key=lambda hand: (hand[2], hand[0]))
        return sum(rank * hand[1] for rank, hand in enumerate(hands, 1))

    def label_to_number(self, cards, wildcard=False):
        mapping = {
            "T": 10,
            "J": 1 if wildcard else 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }

        return [int(mapping.get(i, i)) for i in cards]

    def get_score(self, cards, wildcard=False):
        types = {
            50: "Five of a kind",
            40: "Four of a kind",
            32: "Full house",
            30: "Three of a kind",
            22: "Two pair",
            20: "One pair",
            10: "High card",
        }
        counter = {}
        cards = list(cards)

        jokers = 0
        if wildcard:
            jokers = cards.count("J")
            cards = [i for i in cards if i != "J"]

        for card in cards:
            counter[card] = cards.count(card)

        _max, _2nd = (sorted(counter.values(), reverse=True) + [0] * 5)[:2]
        rank_score = 10 * (_max + jokers) + _2nd
        rank_score = max(i for i in types.keys() if i <= rank_score)

        # using rank_score as the part of the key to sort the hands
        # and types[rank_score] for the debug purpose
        return rank_score, types[rank_score]
