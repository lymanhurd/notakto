"""The implementation of web commands for cribbage."""

from bottle import abort
from crib_player import create_player
from crib_utils import DECK, card_number
from score import scores, score_sequence


def cribbage_command(command, query):
    """Central method to control cribbage commands."""
    player = create_player()  # can optionally give level...defaults  to highest
    comp_score = int(query.get('comp_score', 0))
    human_score = int(query.get('human_score', 0))
    # needed for "play" and "score" methods.
    start_card = card_number(query.get('start', 'AC'))  # Default provided because
    # "play" method currently ignores this parameter.
    # relevant to "discard" and "play"
    computer_dealt = query.get('dealer', 'C').upper() == 'C'
    # used by "discard", "play"
    hand = [card_number(c) for c in query.hand.split(',')]

    # Given six dealt cards, choose two to discard to the crib.
    if command.lower() == 'discard':
        assert len(hand) == 6
        assert len(set(hand)) == 6  # check for duplicates
        discards = player.discard(hand, computer_dealt, human_score, comp_score)
        return ','.join([DECK[c] for c in discards])
    elif command.lower() == 'play':
        comp_cards = [card_number(c) for c in query.comp_cards.split(',')]
        human_cards = [card_number(c) for c in query.human_cards.split(',')]
        assert len(comp_cards) + len(hand) == 4
        assert len(set(comp_cards + human_cards + hand + [start_card])) == (5 +
            len(human_cards))  # check for duplicates
        return DECK[player.play(comp_cards, human_cards, hand, computer_dealt,
                                human_score, comp_score, start_card)]
    elif command.lower() == 'score':  # score and sequence are convenience methods
        assert len(hand) == 4
        crib = None
        if query.get('crib', ''):
            crib = [card_number(c) for c in query.crib.split(',')]
            assert len(crib) == 4
        return ','.join(map(str, scores(hand, crib, start_card)))
    elif command.lower() == 'sequence':
        seq = [card_number(c) for c in query.seq.split(',')]
        assert len(seq) == len(set(seq))  # check for duplicates
        return str(score_sequence(seq))
    else:
        abort(400, 'Unknown cribbage command: {}.'.fmt(command))
