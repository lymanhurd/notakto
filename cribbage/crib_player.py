"""Logic behind computer players."""

from crib_expected_values import expected_crib
from crib_utils import card_value, filter_valid
from score import score, score_sequence


_RESPONSE_WEIGHT = 0  # probability of the best response to a played card


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
    def next_card(self, hand, seq, is_dealer, dscore, pscore, start):
        valid = filter_valid(hand, seq)
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
        best_score = -1
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


    def next_card(self, hand, seq, is_dealer, dscore, pscore, start):
        valid = filter_valid(hand, seq)
        if len(valid) == 0:
            return 0, True  # Go
        else:
            return max(valid, key=lambda c: self._priority(seq, c)), False


    # Pick highest scoring cards and resolve ties in favor of highest card.
    def _priority(self, seq, card):
        expected_score = score_sequence(seq + [card])
        best_response = 0
        for response in range(13):
            response_score = score_sequence(seq + [card, response])
            if response_score > best_response:
                best_response = response
        expected_score -= _RESPONSE_WEIGHT * best_response
        return 100*expected_score + card_value(card)
