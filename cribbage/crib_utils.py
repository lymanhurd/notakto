"""Helper routines for interfacing between web app and cribbage AI."""
from typing import List

from cribbage.deck import card_points


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
