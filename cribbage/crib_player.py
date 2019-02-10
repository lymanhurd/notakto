"""Logic behind computer players."""

import logging

from crib_expected_values import expected_crib
from crib_utils import card_value, filter_valid, seq_count
from score import score, score_sequence


def create_player(level=1, name=''):
    """Return a cribbage player of the requested level."""
    if level == 1:
        return StandardPlayer(name)
    elif level == 2:
        return StandardPlusPlayer(name)
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
        self.discarded = []
        self.passed = False
        self.start = 0
        
    def next_card(self, seq, cur_count, **kwargs):
        valid = filter_valid(self.hand, seq, cur_count)

        if len(valid) == 0:
            self.passed = True
            return 0, True  # Go
        else:
            self.passed = False
            return max(valid, key=lambda c: self._priority(c, seq)), False

    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self, is_dealer, unused_opponent_score):
        """Choose two cards to discard to crib from a hand of six."""
        assert len(self.hand) == 6
        self.discarded = self.hand[:2]
        self.hand = self.hand[2:]
        return self.hand[:2]

    def add(self, points):
        self.score += points
        if self.score > 120:
            raise GameOver()

    def _priority(self, card, unused_seq):
        return card_value(card)
        


class StandardPlayer(BasePlayer):
    def discard(self, is_dealer, unused_opponent_score):
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
        self.discarded = best_discards
        return best_discards


    # Pick highest scoring cards and resolve ties in favor of highest card.
    def _priority(self, card, seq):
        expected_score = score_sequence(seq + [card])
        return 100*expected_score + card_value(card)


class StandardPlusPlayer(StandardPlayer):
    # Pick highest scoring cards and resolve ties in favor of highest card.
    # Account for possible opponent comeback.
    def _priority(self, card, seq):
        expected_score = score_sequence(seq + [card])
        # if len is 7 there is no next card
        if len(seq) >= 7:
            return expected_score

        # compute the expected response
        responses = [(response, score_sequence(seq + [card, response]))
                     for response in range(13)]
        responses = [r for r in responses if r[1] > 0]
        responses.sort(key=lambda x: x[1], reverse=True)

        logging.info('Seq = %s', [c % 13 for c in seq + [card]])
        logging.info('Responses %s', responses)

        # to calculate how likely the opponent is to hold a given card we
        # figure out how many cards of that value have not been seen
        seen_count = 13 * [0]
        seen_cards = self.hand + self.discarded + [self.start]
        assert len(seen_cards) == 7
        seen_cards = set(seen_cards + seq)  # Add the opponents cards.

        logging.info('Cards seen %s', sorted([c % 13 for c in seen_cards]))
        num_cards_seen = len(seen_cards)
        opponents_cards_held =  11 - num_cards_seen  # 4 - (num_cards_seen - 7)

        # we know about our initial 6 cards and the start card
        # the difference has to be the opponent's
        logging.info('opponents_cards_held %s', opponents_cards_held)

        for c in seen_cards:
            seen_count[c % 13] += 1
        card_probs = [(4 - s)/(52 - num_cards_seen) for s in seen_count]
        logging.info('Card probabilities %s', card_probs)

        if opponents_cards_held > 0:
            logging.info('Expected score %s', expected_score)
            # we assume that the opponent will always make the play
            # that maximizes their score, so getting the second highest
            # score means that the opponent has that card and no better
            # card
            p = 0
            for r in responses:
                p += card_probs[r[0]]
                coeff = 1 - (1 - p)**opponents_cards_held
                expected_score -= r[1] * coeff
                logging.warning('r = %s p = %s coeff = %s cards = %s',
                                r, p, coeff, opponents_cards_held)
                logging.info('new expected score %s', expected_score)

        return 100*expected_score + card_value(card)
