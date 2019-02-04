"""Logic behind computer players."""

import logging

from crib_expected_values import expected_crib
from crib_utils import card_value, filter_valid, seq_count
from score import score, score_sequence


_RESPONSE_WEIGHT = 1


def create_player(level=1, name=''):
    """Return a cribbage player of the requested level."""
    if level == 1:
        return StandardPlayer(name)
    else:
        return BasePlayer(name)


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


# exception marking the game over
class GameOver(Exception):
    pass


class BasePlayer():
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.wins = 0
        self.hand = []
        self.passed = False
        
    def next_card(self, seq, cur_count, **kwargs):
        valid = filter_valid(self.hand, seq, cur_count)

        if len(valid) == 0:
            self.passed = True
            return 0, True  # Go
        else:
            self.passed = False
            return max(valid, key=lambda c: self._priority(c, seq)), False

        # num_cards = 4 - len(seq) + len(set(self.hand).intersection(seq))
        # seen = 13 * [0]
        # for c in set(self.hand + seq + [start]):
        #     seen[c % 13] += 1

        # response_scores = [score_sequence(seq + [card, response])
        #                    for response in range(13)]
        # expected_response = 0
        # expected_score -= _RESPONSE_WEIGHT * expected_response
    
    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self, is_dealer, unnused_opponent_score):
        """Choose two cards to discard to crib from a hand of six."""
        assert len(self.hand) == 6
        self.hand = self.hand[2:]
        return self.hand[:2]

    def add(self, points):
        self.score += points
        if self.score > 120:
            raise GameOver()

    def _priority(self, card, unused_seq):
        return card_value(card)
        


class StandardPlayer(BasePlayer):
    def discard(self, is_dealer, opponent_score):
        """Choose two cards to discard to crib from a hand of six.

        Pick two cards that maximize potential score"""
        assert len(self.hand) == 6
        best_score = -9999
        crib_coeff = 13 if is_dealer else -13
        for d in _DIVISIONS:
            total = 0
            discards = [self.hand[i] for i in range(6) if d[i]]
            kept = [self.hand[i] for i in range(6) if not d[i]]
            for start in range(13):
                total += score(kept, start)
            total += crib_coeff * expected_crib(discards)
            if total > best_score:
                best_discards = discards
                best_kept = kept
                best_score = total
        self.hand = best_kept
        return best_discards


    # Pick highest scoring cards and resolve ties in favor of highest card.
    def _priority(self, card, seq):
        expected_score = score_sequence(seq + [card])
        return 100*expected_score + card_value(card)
