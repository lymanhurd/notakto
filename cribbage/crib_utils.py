"""Helper routines for interfacing between web app and AI."""

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 10)] + ['0', 'J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]


def card_number(name):
    return -1 if not name else DECK.index(name[-2:].upper()) # map "10H" to "0H" for example.


def card_value(card):
    return min(10, 1 + card % 13)


def filter_valid(hand, seq):
    cur_count = 0
    for card in seq:
        cur_count += card_value(card)
        if cur_count == 31:
            cur_count = 0
        elif cur_count > 31:
            cur_count = card_value(card)
    return [c for c in hand if cur_count + card_value(c) <= 31]
