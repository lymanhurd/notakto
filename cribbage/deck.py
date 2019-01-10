"""Class representing a deck of cards."""
import logging
import random


class Deck():

    def __init__(self):
        random.seed('deterministic')
        self.deck = list(range(52))
        self.shuffle()
        self.idx = 0

    def shuffle(self):
        random.shuffle(self.deck)
        self.idx = 0

    def deal(self, n):
        cards = self.deck[self.idx: self.idx + n]
        self.idx += n
        assert self.idx < 52
        return cards

    def reset(self):
        random.seed('deterministic')
