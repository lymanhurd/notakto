"""Helper routines for interfacing between web app and AI."""

import logging

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for n in CARD_NAMES for s in SUITS]


def card_number(name):
    return -1 if not name else DECK.index(name.upper())


def card_value(card):
    return min(10, 1 + card % 13)


def filter_valid(hand, seq, cur_count):
    return [c for c in hand if cur_count + card_value(c) <= 31 and c not in seq]


def seq_count(seq):
    cur_count = 0
    for card in seq:
        cur_count += card_value(card)
        if cur_count == 31:
            cur_count = 0
        elif cur_count > 31:
            cur_count = card_value(card)
    return cur_count


def hand_string(hand):
    return ' '.join([DECK[c] for c in hand])
