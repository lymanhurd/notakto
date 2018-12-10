import logging
from crib_utils import card_value, merge



def play(comp_cards, human_cards, hand, computer_dealt, human_score, comp_score,
         start_card):
    if computer_dealt:
        merged = merge(comp_cards, human_cards)
    else:
        merged = merge(human_cards, comp_cards)
    logging.info('merged = %s' % merged)
    count = sum(card_value(c) for c in merged)
    return card_to_play(count, hand)


# .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
def discard(hand, computer_dealt, human_score, player_score):
    """Choose two cards to discard to crib from a hand of six."""
    return hand[:2]

def card_to_play(count, hand):
    logging.info('hand=%s' % hand)
    for h in hand:
        if card_value(h) + count <= 31:
            return h
    return 'go'
