from crib_utils import card_value, merge
from score import score, score_sequence

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
    def play(self, comp_cards, human_cards, hand, computer_dealt, unused_human_score,
             unused_comp_score, unused_start_card):
        _, cur_count = merge(comp_cards, human_cards, computer_dealt)
        valid = [h for h in hand if card_value(h) + cur_count <= 31]
        if not valid:
            return 'go'
        else:
            return max(valid, key=card_value)


    # .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
    def discard(self, hand, computer_dealt, human_score, player_score):
        """Choose two cards to discard to crib from a hand of six."""
        return hand[:2]


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
            if total > best_score:
                best_div = d
                best_score = total
        return [hand[i] for i in range(6) if best_div[i]]

    def play(self, comp_cards, human_cards, hand, computer_dealt, unused_human_score,
             unused_comp_score, unused_start_card):
        merged, cur_count = merge(comp_cards, human_cards, computer_dealt)
        valid = [h for h in hand if card_value(h) + cur_count <= 31]
        if not valid:
            return 'go'
        else:
            return max(valid, key=lambda c: self._priority(merged, c))

    # Pick highest scoring cards and resolve ties in favor of highest card.
    def _priority(self, merged, card):
        return 100*score_sequence(merged + [card]) + card_value(card)
