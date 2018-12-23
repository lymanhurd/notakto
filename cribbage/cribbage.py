"""The implementation of web commands for cribbage."""

import logging

from bottle import abort
from crib_player import create_player
from crib_utils import DECK, card_number
from score import score, score_sequence


def _assert_no_dups(cards):
    logging.debug('dupes checking %s', cards)
    assert len(cards) == len(set(cards))


def cribbage_command(command, query):
    """Central method to control cribbage commands."""
    player = create_player()  # can optionally give level...defaults  to highest
    comp_score = int(query.get('comp_score', 0))
    human_score = int(query.get('human_score', 0))
    # needed for "play" and "score" methods.
    start_card = card_number(query.get('start', ''))
    # relevant to "discard" and "play"
    computer_dealt = query.get('dealer', 'C').upper() == 'C'
    # used by "discard", "play"
    hand = [card_number(c) for c in query.get('hand', '').split(',') if c]

    # Given six dealt cards, choose two to discard to the crib.
    if command.lower() == 'discard':
        assert len(hand) == 6
        _assert_no_dups(hand)
        discards = player.discard(hand, computer_dealt, human_score, comp_score)
        return ','.join([DECK[c] for c in discards])
    elif command.lower() == 'play':
        comp_cards = [card_number(c) for c in query.get('comp_cards','').split(',') if c]
        human_cards = [card_number(c) for c in query.get('human_cards','').split(',') if c]
        assert len(comp_cards) + len(hand) == 4
        _assert_no_dups(comp_cards + human_cards + hand + [start_card])
        return DECK[player.play(comp_cards, human_cards, hand, computer_dealt,
                                human_score, comp_score, start_card)]
    elif command.lower() == 'score':  # score and sequence are convenience methods
        score_dict = {}
        hand1, hand2, crib = [], [], []
        if 'hand1' in query:
            hand1 = [card_number(c) for c in query.get('hand1', '').split(',') if c]
            assert len(hand1) == 4
            score_dict['hand1'] = score(hand1, start_card, False)
        if 'hand2' in query:
            hand2 = [card_number(c) for c in query.get('hand2', '').split(',') if c]
            assert len(hand2) == 4
            score_dict['hand2'] = score(hand2, start_card, False)
        if 'crib' in query:
            crib = [card_number(c) for c in query.get('crib', '').split(',') if c]
            assert len(crib) == 4
            score_dict['crib'] = score(crib, start_card, True)
        _assert_no_dups(hand1 + hand2 + crib + [start_card])
        return score_dict
    elif command.lower() == 'sequence':
        seq = [card_number(c) for c in query.get('seq', '').split(',') if c]
        _assert_no_dups(seq)
        return str(score_sequence(seq))
    else:
        abort(400, 'Unknown cribbage command: {}.'.fmt(command))
