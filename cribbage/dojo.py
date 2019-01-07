"""Framework for comparing two players."""

import logging

from crib_player import create_player
from deck import Deck
from score import score, score_sequence


_NUM_GAMES = 1


def playoff(player1, player2, num_games):
    # The stronger (new) player is assumed to go second so we record wins/margin
    # from Player 2's point of view.

    # Play games twice once from each side.
    wins, margin = 0, 0
    deck = Deck()
    for i in range(num_games):
        deck.shuffle()

        game_win, game_margin = play_game(deck, player1, player2)
        wins += game_win
        margin += game_margin

        # reverse roles
        deck.reset()
        game_win, game_margin = play_game(deck, player2, player1)
        wins += 1 - game_win
        margin -= game_margin
    return wins, margin


def play_game(deck, dealer, pone):
    dscore, pscore = 0, 0
    while dscore < 121 and pscore < 121:
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
    pscore += score(phand)
    if pscore > 120:
        return dscore, pscore
    dscore += score(dhand)
    dscore += score(crib)
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
        card, go = dealer.next_card(dhand, seq, True, dscore, pscore, start)
        if not go:
            seq.append(card)
            cards_played += 1
            dscore += score_sequence(seq)
            if dscore > 120:
                return dscore, pscore
            pscore += score_sequence(seq)
    return dscore, pscore


if __name__ == '__main__':
    player1 = create_player(level=0)
    player2 = create_player(level=1)
    wins, margin = playoff(player1, player2, _NUM_GAMES)
    logging.info('Win percentage = {} margin {}'.fmt((100.0 * wins)/_NUM_GAMES,
                 margin))
