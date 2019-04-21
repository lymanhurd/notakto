"""Class representing a deck of cards."""
import logging
import random

from time import time
from typing import List, Optional, Tuple


class Deck(object):
    def __init__(self, seed: Optional[str] = None):
        self.seed = seed or str(time())
        logging.debug('seed = %s', self.seed)
        random.seed(self.seed)
        self.deck = list(range(52))
        self.shuffle()
        self.idx = 0

    def shuffle(self) -> None:
        random.shuffle(self.deck)
        self.idx = 0

    def deal(self, n: int) -> List[int]:
        cards = self.deck[self.idx: self.idx + n]
        self.idx += n
        return cards


SUITS: List[str] = ['C', 'D', 'H', 'S']
CARD_NAMES: List[str] = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK: List[str] = [n + s for n in CARD_NAMES for s in SUITS]
JACK: int = 10


def card_number(name: str) -> int:
    return -1 if not name else DECK.index(name.upper())


def card_points(card: int) -> int:
    return min(10, 1 + card // 4 % 13)


def suit(card: int) -> int:
    return card % 4


def value(card: int) -> int:
    return card // 4 % 13


def seq_string(seq: List[int], sep: str = ' ') -> str:
    return sep.join([DECK[c] for c in seq])


def hand_string(hand: List[int], sep: str = ' ') -> str:
    return seq_string(sorted(hand), sep)


def random_draw() -> Tuple[int, int]:
    c1, c2 = 0, 0
    while value(c1) == value(c2):
        c1, c2 = random.randint(0, 51), random.randint(0, 51)
    return c1, c2
