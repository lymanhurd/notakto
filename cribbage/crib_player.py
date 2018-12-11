import logging
from crib_utils import card_value, merge
from score import score


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
    def play(self, comp_cards, human_cards, hand, computer_dealt, unused_human_score,
             unused_comp_score, unused_start_card):
        if computer_dealt:
            merged = merge(comp_cards, human_cards)
        else:
            merged = merge(human_cards, comp_cards)
        logging.info('merged = %s' % merged)
        count = sum(card_value(c) for c in merged)
        for h in hand:
            if card_value(h) + count <= 31:
                return h
        return 'go'

    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self, hand, computer_dealt, human_score, player_score):
        """Choose two cards to discard to crib from a hand of six."""
        return hand[:2]

    def _card_to_play(self, count, hand):
        logging.info('hand=%s' % hand)


class StandardPlayer(BasePlayer):
    def discard(self, hand, unused_computer_dealt, unused_human_score, unused_player_score):
        """Choose two cards to discard to crib from a hand of six.

        Pick two cards that maximize potential score (independent of crib)"""
        best_score = -1
        best_div = 0
        for d in _DIVISIONS:
            total = 0
            for start in range(13):
                total += score([hand[i] for i in range(6) if not d[i]], start)
            if total/13.0 > best_score:
                best_div = d
                best_score = total/13.0
        return [hand[i] for i in range(6) if best_div[i]]
