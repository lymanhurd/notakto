"""Logic behind computer players."""

import logging

from crib_expected_values import expected_crib
from crib_utils import card_value, filter_valid
from score import score, score_sequence


_RESPONSE_WEIGHT = 1


def create_player(level=1):
    """Return a cribbage player of the requested level."""
    if level == 1:
        return StandardPlayer()
    else:
        return BasePlayer()


_DIVISIONS = (
    (True, True, False, False, False, False), (True, False, True, False, False, False),
    (True, False, False, True, False, False), (True, False, False, False, True, False),
    (True, False, False, False, False, True), (False, True, True, False, False, False),
    (False, True, False, True, False, False), (False, True, False, False, True, False),
    (False, True, False, False, False, True), (False, False, True, True, False, False),
    (False, False, True, False, True, False), (False, False, True, False, False, True),
    (False, False, True, False, True, False), (False, False, True, False, False, True),
    (False, False, False, True, True, False), (False, False, False, True, False, True),
    (False, False, False, False, True, True))

class BasePlayer():
    def next_card(self, hand, seq, is_dealer, dscore, pscore, start, go):
        valid = filter_valid(hand, seq, go)
        if len(valid) == 0:
            return 0, True  # Go
        else:
            return max(valid, key=card_value), False


    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self, hand, is_dealer, dscore, pscore):
        """Choose two cards to discard to crib from a hand of six."""
        return hand[:2], hand[2:]


class StandardPlayer(BasePlayer):
    def discard(self, hand, is_dealer, dscore, pscore):
        """Choose two cards to discard to crib from a hand of six.

        Pick two cards that maximize potential score"""
        best_score = -9999
        crib_coeff = 13 if is_dealer else -13
        for d in _DIVISIONS:
            total = 0
            discards = [hand[i] for i in range(6) if d[i]]
            kept = [hand[i] for i in range(6) if not d[i]]
            for start in range(13):
                total += score(kept, start)
            total += crib_coeff * expected_crib(discards)
            if total > best_score:
                best_discards = discards
                best_kept = kept
                best_score = total
        return best_discards, best_kept


    def next_card(self, hand, seq, is_dealer, dscore, pscore, start, new_start):
        valid = filter_valid(hand, seq, new_start)
        if len(valid) == 0:
            return 0, True  # Go
        num_cards = 4 - len(seq) + len(set(hand).intersection(seq))
        seen = 13 * [0]
        for c in set(hand + seq + [start]):
            seen[c % 13] += 1
        return max(valid, key=lambda c: self._priority(c, seq)), False


    # Pick highest scoring cards and reseolve ties in favor of highest card.
    def _priority(self, card, seq):
        expected_score = score_sequence(seq + [card])
        response_scores = [score_sequence(seq + [card, response])
                           for response in range(13)]
        expected_response = 0
        expected_score -= _RESPONSE_WEIGHT * expected_response
        return 100*expected_score + card_value(card)
