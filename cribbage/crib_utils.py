"""Helper routines for interfacing between web app and cribbage AI."""
from typing import List


SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for n in CARD_NAMES for s in SUITS]
JACK = 10


def card_number(name: str) -> int:
    return -1 if not name else DECK.index(name.upper())


def card_points(card: int) -> int:
    return min(10, 1 + (card // 4) % 13)


def suit(card: int):
    return card % 4


def value(card: int):
    return (card // 4) % 13


def filter_valid(hand: List[int], seq: List[int], cur_count: int) -> List[int]:
    return [c for c in hand if cur_count + card_points(c) <= 31 and c not in seq]


def seq_count(seq: List[int]) -> int:
    cur_count = 0
    for card in seq:
        cur_count += card_points(card)
        if cur_count == 31:
            cur_count = 0
        elif cur_count > 31:
            cur_count = card_points(card)
    return cur_count


def seq_string(seq: List[int]) -> str:
    return ' '.join([DECK[c] for c in seq])


def hand_string(hand: List[int]) -> str:
    return seq_string(sorted(hand))
