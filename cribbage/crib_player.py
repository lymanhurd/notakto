"""Logic behind computer players."""
import logging

from cribbage.crib_expected_values import expected_crib
from cribbage.crib_utils import filter_valid, seq_count
from cribbage.deck import card_number, card_points, seq_string, hand_string
from cribbage.score import score, score_sequence
from typing import List, Tuple

_DIVISIONS: Tuple[Tuple[bool]] = (
    (True, True, False, False, False, False), (True, False, True, False, False, False),
    (True, False, False, True, False, False), (True, False, False, False, True, False),
    (True, False, False, False, False, True), (False, True, True, False, False, False),
    (False, True, False, True, False, False), (False, True, False, False, True, False),
    (False, True, False, False, False, True), (False, False, True, True, False, False),
    (False, False, True, False, True, False), (False, False, True, False, False, True),
    (False, False, True, False, True, False), (False, False, True, False, False, True),
    (False, False, False, True, True, False), (False, False, False, True, False, True),
    (False, False, False, False, True, True))


# Exception marking the game over
class GameOver(Exception):
    pass


class Player(object):
    def __init__(self):
        self.name: str = type(self).__name__
        self.score: int = 0
        self.hand: List[int] = []
        self.discarded: List[int] = []
        self.passed: bool = False
        self.opponent_passed: bool = False
        self.start: int = 0
        self.is_dealer: bool = False
        self.wins: int = 0

    def add(self, points: int) -> None:
        self.score += points
        if self.score > 120:
            raise GameOver()

    def discard(self) -> List[int]:
        self.discarded = self.choose_discards(self.is_dealer, self.hand)
        return self.discarded

    @staticmethod
    def choose_discards(is_dealer: bool, hand: List[int]) -> List[int]:
        raise NotImplementedError

    def next_card(self, seq: List[int]) -> Tuple[int, bool]:
        cur_count = seq_count(seq)
        valid = filter_valid(self.hand, seq, cur_count)
        num_valid = len(valid)

        if num_valid == 0 and self.passed and self.opponent_passed:
            logging.info('New round.')
            valid = filter_valid(self.hand, seq, 0)
            num_valid = len(valid)

        if num_valid == 0:
            self.passed = True
            return 0, True  # Go
        else:
            self.passed = False
            if num_valid == 1:
                return valid[0], False
            else:
                return self.choose_card(valid, seq), False

    def choose_card(self, valid: List[int], seq: List[int], **kwargs) -> int:
        raise NotImplementedError


class HumanPlayer(Player):
    @staticmethod
    def choose_discards(is_dealer: bool, hand: List[int]) -> List[int]:
        """Choose two cards to discard to crib from a hand of six."""
        assert len(hand) == 6
        discarded = []
        while not discarded:
            whose = 'Your' if is_dealer else 'Opponent\'s'
            d = input('%s crib: Hand [%s] Choose discards: ' % (whose, hand_string(hand)))
            cards = [card_number(c) for c in d.split()]
            if (len(cards) != 2 or len(set(cards)) != 2 or
                    cards[0] not in hand or
                    cards[1] not in hand):
                print('Need to discard two cards from hand')
            else:
                discarded = cards
        return discarded[:]

    def choose_card(self, valid: List[int], seq: List[int], **kwargs) -> int:
        while True:
            d = input('Choose card: seq [%s] hand [%s]: ' % (seq_string(seq), hand_string(valid)))
            c = card_number(d)
            if c in self.hand:
                return c
            else:
                print("Please choose a card in your hand.")


class BasicPlayer(Player):
    def choose_card(self, valid: List[int], seq: List[int], **kwargs) -> int:
        return max(valid, key=lambda c: self._priority(c, seq))

    @staticmethod
    def choose_discards(is_dealer: bool, hand: List[int]) -> List[int]:
        """Choose two cards to discard to crib from a hand of six."""
        assert len(hand) == 6
        discarded = hand[:2]
        return discarded

    # The basic algorithm always plays the highest count among legal cards.
    def _priority(self, card, unused_seq):
        return card_points(card)


class StandardPlayer(BasicPlayer):
    @staticmethod
    def choose_discards(is_dealer: bool, hand: List[int]) -> List[int]:
        """Choose two cards to discard to crib from a hand of six.

        Pick two cards that maximize potential score"""
        assert len(hand) == 6
        best_score = -9999
        best_discards = None
        crib_coefficient = 13 if is_dealer else -13
        for d in _DIVISIONS:
            total = 0
            discards = [hand[i] for i in range(6) if d[i]]
            kept = [hand[i] for i in range(6) if not d[i]]
            for start in range(13):
                total += score(kept, start)
            total += crib_coefficient * expected_crib(discards)
            if total > best_score:
                best_discards = discards
                best_score = total
        return best_discards

    # Pick highest scoring cards and resolve ties in favor of highest card.
    def _priority(self, card: int, seq: List[int]) -> int:
        expected_score = score_sequence(seq, card)
        return 100 * expected_score + card_points(card)


class StandardPlusPlayer(StandardPlayer):
    # Pick highest scoring cards and resolve ties in favor of highest card.
    # Account for expected value of opponent's response.
    def _priority(self, card: int, seq: List[int]) -> int:
        expected_score = score_sequence(seq, card)
        # if len is 7, there is no next card
        if len(seq) >= 7:
            return 100 * expected_score + card_points(card)

        # compute the expected value of the opponent's response
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
        opponents_cards_held = 11 - num_cards_seen  # 4 - (num_cards_seen - 7)

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
        return 100 * expected_score + card_points(card)


def create_player(level=2) -> Player:
    """Return a cribbage player of the requested level."""
    if level == 0:
        return BasicPlayer()
    elif level == 1:
        return StandardPlayer()
    elif level == 2 or level == -1:  # -1 signifies max
        return StandardPlusPlayer()
    else:
        return BasicPlayer()
