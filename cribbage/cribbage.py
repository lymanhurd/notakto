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
    dealer_score = int(query.get('dealer_score', 0))
    pone_score = int(query.get('pone_score', 0))
    # needed for "play" and "score" methods.
    start_card = card_number(query.get('start', ''))
    # relevant to "discard" and "play"
    is_dealer = query.get('dealer', 'C').upper() == 'C'
    # used by "discard", "play"
    hand = [card_number(c) for c in query.get('hand', '').split(',') if c]

    # Given six dealt cards, choose two to discard to the crib.
    if command.lower() == 'discard':
        assert len(hand) == 6
        _assert_no_dups(hand)
        discards, _  = player.discard(hand, is_dealer, dealer_score, pone_score)
        return ','.join([DECK[c] for c in discards])
    elif command.lower() == 'play':
        hand = [card_number(c) for c in query.get('hand','').split(',') if c]
        assert len(hand) == 4
        seq = [card_number(c) for c in query.get('seq','').split(',') if c]
        assert len(seq) < 8
        new_start = query.get('new_start', 'False')
        _assert_no_dups(hand + [start_card])
        _assert_no_dups(seq + [start_card])
        card, go = player.next_card(hand, seq, is_dealer, dealer_score, pone_score, start_card, bool(new_start))
        return 'go' if go else DECK[card]
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
