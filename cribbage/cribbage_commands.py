"""The implementation of web commands for cribbage."""

import logging

from bottle import abort
from cribbage.crib_player import create_player
from cribbage.crib_utils import DECK, card_number
from cribbage.score import score, score_sequence
from typing import List, Any


def _assert_no_dups(cards: List[int]) -> None:
    logging.debug('dupes checking %s', cards)
    assert len(cards) == len(set(cards))


def cribbage_command(command: str, query: Any):
    """Central method to control cribbage commands."""
    player = create_player()  # can optionally give level...defaults  to highest
    dealer_score = int(query.get('dealer_score', 0))
    pone_score = int(query.get('pone_score', 0))
    # needed for "play" and "score" methods.
    start_card = card_number(query.get('start', ''))
    # relevant to "discard" and "play"
    is_dealer = query.get('dealer', 'C').upper() == 'C'
    # used by "discard", "play"
    player.hand = [card_number(c) for c in query.get('hand', '').split(',') if c]

    # Given six dealt cards, choose two to discard to the crib.
    if command.lower() == 'discard':
        assert len(player.hand) == 6
        _assert_no_dups(player.hand)
        discards = player.discard()
        return ','.join([DECK[c] for c in discards])
    elif command.lower() == 'play':
        hand = [card_number(c) for c in query.get('hand','').split(',') if c]
        assert len(hand) == 4
        seq = [card_number(c) for c in query.get('seq','').split(',') if c]
        assert len(seq) < 8
        new_start = query.get('new_start', 'False') == 'True' 
        _assert_no_dups(hand + [start_card])
        _assert_no_dups(seq + [start_card])
        card, go = player.next_card(seq, is_dealer, 0, start_card, new_start)
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
