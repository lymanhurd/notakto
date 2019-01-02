"""Framework for comparing two players."""

import logging

from crib_player import create_player
from deck import Deck
from game import play_hand


_NUM_GAMES = 1


def playoff(player1, player2):
    # The sstronger (new) player is assumed to go second so we record wins/margin from 
    # Player 2's point of view.
    wins, margin  = 0, 0
    deck = Deck()



    def playoff(player1, player2, num_games):
        # Play games twice once from each side. 
        for i in xrange(num_games):
            score1, score2 = 0, 0
            while score1 < 121 and score2 < 121:
                deck.shuffle()
                hand1 = deck.deal(6)
                hand2 = deck.deal(6)
                start = deck.deal(1)

                # The first player is always the dealer.
                score1, score2 = play_hand(player1, hand1, score1, player2, hand2, score2, start)

                # Game over.  Only one player can have passed 120!
                assert score1 < 121 or score2 < 121

                if score2 > score1:
                    logging.debug('Player 2 wins: (%d, %d)', score1, score2)
                    wins += 1
                else:
                    logging.debug('Player 1 wins: (%d, %d)', score1, score2)

                margin += score2 - score1

        return wins, margin


if __name__ == '__main__':
    player1 = create_player(level=0)
    player2 = create_player(level=0)
    wins, margin = playoff(player1, player2, _NUM_GAMES)
    logging.info('Win percentage = %d margin %d' % (100.0 * wins)/_NUM_GAMES)
