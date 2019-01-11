"""Play a game between two players."""

import logging


class GameOver(Exception):
    pass


def play_hand(player1, h1, score1, player2, h2, score2, start, player1_deals):
    try:
        if start % 13 == 10:  # Start card is Jack, score "his heels".
            if player1_deals:
                score1, score2 = increment_scores(2, 0 )
            else:
                increment_scores(0, 2)

        discard1, hand1 = player1.discard(h1)
        discard2, hand2 = player1.discard(h2)
        crib = discard1 + discard2

        logging.debug('H1: %s H2 %s Crib: %s', hand1, hand2, crib)
        

        # score opponent's hand
        increment_scores(2, 0 )

        # score dealer's hand

        # score crib

    except GameOver:
        return score1, score2
    assert False # should not get here
    return 0, 0
