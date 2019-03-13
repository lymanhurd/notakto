"""Logic behind computer players."""

from __future__ import division

import logging

from crib_expected_values import expected_crib
from crib_utils import card_number, card_value, filter_valid, seq_count, hand_string
from score import score, score_sequence


def create_player(level=2, is_dealer=True):
    """Return a cribbage player of the requested level."""
    if level == 0:
        return HumanPlayer(is_dealer)
    elif level == 1:
        return StandardPlayer(is_dealer)
    elif level == 2 or level == -1:  # -1 signifies max
        return StandardPlusPlayer(is_dealer)
    else:
        return BasicPlayer(is_dealer)


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


class BasePlayer(object):
    DEFAULT_NAME = 'Base'

    def __init__(self, is_dealer):
        self.name = self.DEFAULT_NAME
        self.score = 0
        self.hand = []
        self.discarded = []
        self.passed = False
        self.start = 0
        self.is_dealer = is_dealer

    def add(self, points):
        logging.info('Adding %s + %d Total %s', self.name, points, self.score)
        self.score += points
        if self.score > 120:
            logging.info('Game Over')
            raise GameOver()
        
    def must_pass(self, seq):
        cur_count = seq_count(seq)
        valid = filter_valid(self.hand, seq, cur_count)
        return len(valid) == 0

class HumanPlayer(BasePlayer):
    DEFAULT_NAME = 'Human'

    def discard(self):
        """Choose two cards to discard to crib from a hand of six."""
        assert len(self.hand) == 6
        if self.is_dealer:
            print("Your crib")
        else:
            print("Opponent's crib")            
        print(hand_string(sorted(self.hand)))
        while not self.discarded:
            d = input('Choose discards: ')
            cards = [card_number(c) for c in d.split()]
            if (len(cards) != 2 or len(set(cards)) != 2 or
                cards[0] not in self.hand or
                cards[1] not in self.hand):
                print('Need to discard two cards from hand')
            else:
                self.discarded = cards
        self.hand.remove(self.discarded[0])
        self.hand.remove(self.discarded[1])        
        return self.discarded[:]

    def next_card(self, seq, cur_count=-1, **kwargs):
        cur_count = seq_count(seq)
        valid = filter_valid(self.hand, seq, cur_count)
        num_valid = len(valid)
        print('Current sequence: %s' % hand_string(seq))

        if num_valid == 0:
            self.passed = True
            return 0, True  # Go
        else:
            self.passed = False
            if num_valid == 1:
                return (valid[0], False)
            else:
                print(hand_string(sorted(valid)))
                while True:
                    d = input('Choose card to play: ')
                    c = card_number(d) 
                    if c in self.hand:
                        self.hand.remove(c)
                        return c, False
                    else:
                        print("Please choose a card in your hand.")


class BasicPlayer(BasePlayer):
    DEFAULT_NAME = 'Alpha'
        
    def next_card(self, seq, cur_count=-1, **kwargs):
        if cur_count == -1:
            cur_count = seq_count(seq)
        valid = filter_valid(self.hand, seq, cur_count)

        num_valid = len(valid)
        if num_valid == 0:
            self.passed = True
            return 0, True  # Go
        else:
            self.passed = False
            if num_valid == 1:
                return (valid[0], False)
            else:
                return (max(valid, key=lambda c: self._priority(c, seq)), False)

    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self):
        """Choose two cards to discard to crib from a hand of six."""
        assert len(self.hand) == 6
        self.discarded = self.hand[:2]
        self.hand = self.hand[2:]
        return self.hand[:2]

    # The basic algorithm always plays the highest count among legal cards.
    def _priority(self, card):
        return card_value(card)


class StandardPlayer(BasicPlayer):
    DEFAULT_NAME = 'Beta'

    def discard(self):
        """Choose two cards to discard to crib from a hand of six.

        Pick two cards that maximize potential score"""
        assert len(self.hand) == 6
        best_score = -9999
        crib_coeff = 13 if self.is_dealer else -13
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
        expected_score = score_sequence(seq, card)
        return 100*expected_score + card_value(card)


class StandardPlusPlayer(StandardPlayer):
    DEFAULT_NAME = 'Gamma'

    # Pick highest scoring cards and resolve ties in favor of highest card.
    # Account for possible opponent response.
    def _priority(self, card, seq):
        expected_score = score_sequence(seq, card)
        # if len is 7 there is no next card
        if len(seq) >= 7:
            return 100*expected_score + card_value(card)

        # compute the expected response
        responses = [(response, score_sequence((seq + [card]), response))
                     for response in range(13)]
        responses = [r for r in responses if r[1] > 0]
        responses.sort(key=lambda x: x[1], reverse=True)

        logging.debug('Seq = %s', [c % 13 for c in seq + [card]])
        logging.debug('Responses %s', responses)

        # to calculate how likely the opponent is to hold a given card we
        # figure out how many cards of that value have not been seen
        seen_count = 13 * [0]
        seen_cards = self.hand + self.discarded + [self.start]
        assert len(seen_cards) == 7
        seen_cards = set(seen_cards + seq)  # Add the opponents cards.

        logging.debug('Cards seen %s', sorted([c % 13 for c in seen_cards]))
        num_cards_seen = len(seen_cards)
        opponents_cards_held =  11 - num_cards_seen  # 4 - (num_cards_seen - 7)

        # we know about our initial 6 cards and the start card
        # the difference has to be the opponent's
        logging.debug('opponents_cards_held %s', opponents_cards_held)

        for c in seen_cards:
            seen_count[c % 13] += 1

        if opponents_cards_held > 0:
            logging.debug('Expected score %s', expected_score)
            # we assume that the opponent will always make the play
            # that maximizes their score, so getting the second highest
            # score means that the opponent has that card and no better
            # card
            denominator = 52 - num_cards_seen
            p = 1.0
            for r in responses:
                numerator = (4 - seen_count[r[0]])/denominator 
                q = (1 - numerator/denominator)**opponents_cards_held
                expected_score -= p * r[1] * (1 - q)
                # We are interested in the conditional probability of
                # a card given that no "better" card has been found,
                # hence we accumulate the probabilities that the previous
                # cards turned up nothing.
                denominator -= seen_count[r[0]]
                p *= q

        return 100*expected_score + card_value(card)
