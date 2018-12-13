from bottle import abort
from crib_player import BasePlayer, StandardPlayer
from crib_utils import DECK, card_number
from score import scores, score_sequence

import logging


def cribbage_command(command, query):
    """Central method to control cribbage commands."""
    player = StandardPlayer()
    comp_score = query.get('comp_score', 0)
    human_score = query.get('human_score', 0)
    start_card = query.get('start', '')
    computer_dealt = query.get('dealer', 'C').upper() == 'C'
    if command.lower() == 'discard':
        cards = [card_number(c) for c in query.hand.split(',')]
        assert len(cards) == 6
        discards = player.discard(cards, computer_dealt, human_score, comp_score)
        return ','.join([DECK[c] for c in discards])
    elif command.lower() == 'play':
        comp_cards = [card_number(c) for c in query.comp_cards.split(',')]
        human_cards = [card_number(c) for c in query.human_cards.split(',')]
        hand = [card_number(c) for c in query.hand.split(',')]
        assert len(comp_cards) + len(hand) == 4
        return DECK[player.play(comp_cards, human_cards, hand, computer_dealt, human_score,
                         comp_score, start_card)]
    elif command.lower() == 'score':  # score and sequence are convenience methods
        start_card = card_number(query.start)
        hand = [card_number(c) for c in query.hand.split(',')]
        assert len(hand) == 4
        crib = None
        if query.get('crib', ''):
            crib = [card_number(c) for c in query.crib.split(',')]
            assert len(crib) == 4
        return ','.join(map(str, scores(hand, crib, start_card)))
    elif command.lower() == 'sequence':
        seq = [card_number(c) for c in query.seq.split(',')]
        return str(score_sequence(seq))
    else:
        abort(400, 'Unknown cribbage command: {}.'.fmt(command))
