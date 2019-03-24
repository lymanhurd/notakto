"""Utilities for scoring hands and sequences."""
import logging

from cribbage.crib_utils import card_points, DECK, JACK, suit, value
from typing import List

# Number of points earned by 0-4 copies of the same card value.
# Includes placeholder values for 5-8.
PAIRS = (0, 0, 2, 6, 12, 0, 0, 0, 0)


def score(hd: List[int], start: int, is_crib: bool = False):
    assert len(hd) == 4
    hand = list(hd[:])
    points = 0
    # nibs
    start_suit = suit(start)
    for h in hand:
        if start_suit == suit(h) and value(h) == JACK:
            points += 1
    logging.debug('nibs: %d', points)
    suit0 = suit(hand[0])
    # flush
    flush = True
    for h in hand[1:]:
        if suit(h) != suit0:
            flush = False
            break
    if flush:
        if suit0 == start_suit:
            points += 5
        elif not is_crib:
            points += 4
    logging.debug('flush: %d', points)
    # all subsequent clauses do not distinguish starter card from hand cards
    hand.append(start)
    # pairs, pair royals, double pair royal
    hist = 13 * [0]
    for h in hand:
        hist[value(h)] += 1
    logging.debug(hist)
    run = 0
    product = 1
    for n in hist:
        points += PAIRS[n]
        logging.debug('pairs: = %d', points)
        # a zero means a run is broken
        if n == 0:
            if run >= 3:
                points += run * product
            run = 0
            product = 1
        else:
            product *= n
            run += 1
    if hist[-1] == 1 and run >= 3:
        points += run * product
    logging.debug('runs: = %d', points)
    # 15's
    points += 2 * _ways_to_make_sum(15, [card_points(h) for h in hand])
    logging.debug('fifteens: %d', points)
    return points


def score_sequence(sequence, card):
    logging.debug('scoring: %s %s', [DECK[c] for c in sequence], DECK[card])
    seq = sequence + [card]
    logging.debug('(1) seq = %s', seq)
    # truncate
    count = 0
    start = 0
    points = 0
    for i, c in enumerate(seq):
        if card_points(c) + count <= 31:
            count += card_points(c)
        else:
            count = card_points(c)
            start = i
    if count == 15 or count == 31:
        points += 2

    seq = seq[start:]
    logging.debug('(2) seq = %s', seq)
    logging.debug('-points = %s', points)

    # check for pair, pair royal, double pair royal
    cv = value(seq[-1])
    run = 1
    for s in reversed(seq[:-1]):
        if cv != value(s):
            break
        else:
            run += 1
    points += PAIRS[run]
    logging.debug('--points = %d', points)
    # check for runs
    if len(seq) >= 3:
        for i in range(min(len(seq), 8), 2, -1):
            if _is_run(seq[-i:]):
                points += i
                break
    logging.debug('---points = %d', points)
    return points


def _ways_to_make_sum(n, l):
    if n <= 0 or len(l) == 0:
        return 0
    if l[0] == n:
        return 1 + _ways_to_make_sum(n, l[1:])
    else:
        return _ways_to_make_sum(n - l[0], l[1:]) + _ways_to_make_sum(n, l[1:])


def _is_run(sub_seq):
    seq_len = len(sub_seq)
    val_seq = [value(s) for s in sub_seq]
    if max(val_seq) - min(val_seq) != seq_len - 1:
        return False
    if len(set(val_seq)) != seq_len:
        return False
    return True

