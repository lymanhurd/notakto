"""Class representing a deck of cards."""
import random


class Deck():

    def __init__(self):
        random.seed('deterministic')
        self.deck = list(range(52))
        self.idx = 0

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, n):
        cards = self.deck[self.idx: self.idx + n]
        self.idx += n
        assert self.idx < 52
        return cards

    def reset(self):
        self.idx = 0
