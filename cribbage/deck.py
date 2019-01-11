"""Class representing a deck of cards."""
import logging
import random

from time import time

class Deck():

    def __init__(self, seed=None):
        self.seed = seed or str(time())
        logging.debug('seed = %s', self.seed)
        random.seed(self.seed)
        self.deck = list(range(52))
        self.shuffle()
        self.idx = 0

    def shuffle(self):
        random.shuffle(self.deck)
        self.idx = 0

    def deal(self, n):
        cards = self.deck[self.idx: self.idx + n]
        self.idx += n
        return cards


