"""Framework for comparing two players."""

from __future__ import division
from __future__ import print_function

import logging

from crib_player import create_player
from deck import Deck
from score import score, score_sequence


# actually we end up playng twice this many
_NUM_GAMES = 1000
_NUM_HANDS = 1000


def play_games(player1, player2, num_games):
    # The stronger (new) player is assumed to go second so we record wins/margin
    # from Player 2's point of view.

    wins, margin = 0, 0
    deck = Deck()
    for i in range(num_games):
        logging.debug('Game %d', i)
        game_win, game_margin = play_game(deck, player1, player2)
        wins += game_win
        margin += game_margin
        logging.debug('(%d, %d)', wins, i - wins)
    return wins, margin


def play_hands(player1, player2, num_hands):
    # The stronger (new) player is assumed to go second so we record wins/margin
    # from Player 2's point of view.

    # Play games twice once from each side.
    margin = 0
    for i in range(num_hands):
        deck = Deck()
        logging.debug('Hand %d', i)
        dhand = deck.deal(6)
        phand = deck.deal(6)
        start = deck.deal(1)[0]

        # Play hand with player2 as dealer.
        dscore2, pscore1 = play_hand(player2, dhand, 0, player1, phand, 0, start)

        # Play hand with player1 as dealer.
        dscore1, pscore2 = play_hand(player1, dhand, 0, player2, phand, 0, start)
        margin += (pscore2 - pscore1) + (dscore2 - dscore1)        
        logging.debug('margin %d', margin)
    return margin


def play_game(deck, dealer, pone):
    dscore, pscore = 0, 0
    while dscore < 121 and pscore < 121:
        deck.shuffle()
        dhand = deck.deal(6)
        phand = deck.deal(6)
        start = deck.deal(1)[0]
        dscore, pscore = play_hand(dealer, dhand, dscore, pone, phand, pscore, start)
    return int(dscore > pscore), dscore - pscore


def play_hand(dealer, dhand, dscore, pone, phand, pscore, start):
    if start % 13 == 10:  # his heels
        dscore += 2
        if dscore > 120:
            return True, 2
    dcrib, dhand = dealer.discard(dhand, True, dscore, pscore)
    pcrib, phand = dealer.discard(phand, False, pscore, dscore)
    crib = dcrib + pcrib
    dscore, pscore = pegging(dealer, dhand, dscore, pone, phand, pscore, start)
    if dscore > 120 or pscore > 120:
        return dscore, pscore
    pscore += score(phand, start)
    if pscore > 120:
        return dscore, pscore
    dscore += score(dhand, start)
    dscore += score(crib, start, is_crib=True)
    return dscore, pscore


def pegging(dealer, dhand, dscore, pone, phand, pscore, start):
    seq = []
    cards_played = 0
    while cards_played < 8:
        card, go = pone.next_card(phand, seq, False, dscore, pscore, start)
        if not go:
            seq.append(card)
            cards_played += 1
            pscore += score_sequence(seq)
            if pscore > 120:
                return dscore, pscore
        else:
            seq = []
        card, go = dealer.next_card(dhand, seq, True, dscore, pscore, start)
        if not go:
            seq.append(card)
            cards_played += 1
            dscore += score_sequence(seq)
            if dscore > 120:
                return dscore, pscore
        else:
            seq = []
    return dscore, pscore


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    player1 = create_player(level=0)
    player2 = create_player(level=1)
    margin = play_hands(player1, player2, _NUM_HANDS)
    print('Average margin ', margin/(2*_NUM_HANDS))
