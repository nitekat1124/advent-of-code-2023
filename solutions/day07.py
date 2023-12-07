from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        hands = [line.split() for line in data]
        hands = [(self.label_to_number(hand[0]), int(hand[1]), self.get_order(hand[0])) for hand in hands]
        hands = sorted(hands, key=lambda hand: (hand[2], hand[0]))
        return sum(rank * hand[1] for rank, hand in enumerate(hands, 1))

    def part2(self, data):
        hands = [line.split() for line in data]
        hands = [(self.label_to_number(hand[0], wildcard=True), int(hand[1]), self.get_order(hand[0], wildcard=True)) for hand in hands]
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

    def get_order(self, cards, wildcard=False):
        orders = {
            5: (6, "5"),
            4: (5, "4"),
            32: (4, "fh"),
            3: (3, "3"),
            22: (2, "2p"),
            2: (1, "1p"),
            1: (0, "h"),
        }
        counter = {}
        cards = list(cards)

        jokers = 0
        if wildcard:
            jokers = cards.count("J")
            cards = [i for i in cards if i != "J"]

        for card in cards:
            counter[card] = cards.count(card)

        if 5 in counter.values() or jokers == 5:
            return orders[5]
        elif 4 in counter.values():
            return orders[4 + jokers]
        elif 3 in counter.values() and 2 in counter.values():
            return orders[32]
        elif 3 in counter.values():
            return orders[3 + jokers]
        elif 2 in counter.values() and list(counter.values()).count(2) == 2:
            return orders[22 + jokers * 10]
        elif 2 in counter.values():
            return orders[2 + jokers]
        else:
            return orders[1 + jokers]
