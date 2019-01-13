"""Framework for comparing two players."""

from __future__ import division
from __future__ import print_function

import logging

from crib_player import create_player
from crib_utils import DECK, hand_string
from deck import Deck
from score import score, score_sequence


# actually we end up playng twice this many
_NUM_GAMES = 1
_NUM_HANDS = 10000


def play_games(player1, player2, num_games=1):
    # The stronger (new) player is assumed to go second so we record wins/margin
    # from Player 2's point of view.
    wins, margin = 0, 0
    for i in range(num_games):
        logging.debug('Game %d', i)
        game_win, game_margin = play_game(player1, player2)
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


def play_game(dealer, pone):
    deck = Deck()
    dscore, pscore = 0, 0
    while dscore < 121 and pscore < 121:
        deck.shuffle()
        dhand = deck.deal(6)
        phand = deck.deal(6)
        start = deck.deal(1)[0]
        dscore, pscore = play_hand(dealer, dhand, dscore, pone, phand, pscore, start)
    return int(dscore > pscore), dscore - pscore


def play_hand(dealer, dhand, dscore, pone, phand, pscore, start):
    logging.info('Start card: %s', DECK[start])
    if start % 13 == 10:  # his heels
        dscore += 2
        logging.info('Heels: dealer %d pone %d', dscore, pscore)
        if dscore > 120:
            return True, 2

    dcrib, dhand = dealer.discard(dhand, True, dscore, pscore)
    logging.info('dealer hand %s discard %s', hand_string(dhand), hand_string(dcrib))
    pcrib, phand = dealer.discard(phand, False, pscore, dscore)
    logging.info('pone   hand %s discard %s\n', hand_string(phand), hand_string(pcrib))    

    dscore, pscore = pegging(dealer, dhand, dscore, pone, phand, pscore, start)

    logging.info('Dealer %d Pone %d', dscore, pscore)
    if dscore > 120 or pscore > 120:
        return dscore, pscore

    pscore += score(phand, start)
    logging.info('pone   hand %s start %s score %d', hand_string(phand), DECK[start], pscore)

    if pscore > 120:
        return dscore, pscore

    dscore += score(dhand, start)
    logging.info('dealer hand %s start %s score %d', hand_string(dhand), DECK[start], dscore)

    crib = dcrib + pcrib
    cscore = score(crib, start, is_crib=True)
    dscore += cscore
    logging.info('crib   hand %s start %s score %d\n', hand_string(crib), DECK[start], cscore)

    logging.info('DEALER %d PONE %d', dscore, pscore)    
    return dscore, pscore


def pegging(dealer, dhand, dscore, pone, phand, pscore, start):
    seq = []
    cards_played = 0
    go_count = 0
    while cards_played < 8:
        # Pone
        if go_count == 2:
            card, go = pone.next_card(phand, seq, False, dscore, pscore, start, True)
            go_count = 0
        else:
            card, go = pone.next_card(phand, seq, False, dscore, pscore, start, False)            
        if go:
            go_count += 1
            if go_count == 1:
                logging.info('pone   -> go (dealer +1)\n')
                dscore += 1
                logging.info('dealer %d pone %d', dscore, pscore)
                if dscore > 120:
                    return dscore, pscore                
        else:
            seq.append(card)
            cardscore = score_sequence(seq)
            logging.info('pone   -> %s (%d)', DECK[card], cardscore)
            pscore += cardscore
            if cardscore:
                logging.info('dealer %d pone %d', dscore, pscore)
            if pscore > 120:
                return dscore, pscore
            cards_played += 1
            if cards_played == 8:
                pscore += 1
                logging.info('dealer %d pone %d', dscore, pscore)
        # Dealer
        if go_count == 2:
            card, go = dealer.next_card(dhand, seq, False, dscore, pscore, start, True)
            go_count = 0
        else:
            card, go = dealer.next_card(dhand, seq, False, dscore, pscore, start, False)
        if go:
            go_count += 1
            if go_count == 1:
                logging.info('dealer -> go (pone +1)\n')
                pscore += 1
                logging.info('dealer %d pone %d', dscore, pscore)
                if pscore > 120:
                    return dscore, pscore                
            else:
                logging.info('dealer -> go\n')
        else:
            seq.append(card)            
            cardscore = score_sequence(seq)
            logging.info('dealer -> %s (%d)', DECK[card], cardscore)
            dscore += cardscore
            if cardscore:
                logging.info('dealer %d pone %d', dscore, pscore)            
            if dscore > 120:
                return dscore, pscore             
            cards_played += 1
            if cards_played == 8:
                dscore += 1
                if cardscore:
                    logging.info('dealer %d pone %d', dscore, pscore)            
    return dscore, pscore


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    player1 = create_player(level=0)
    player2 = create_player(level=1)
#    margin = play_hands(player1, player2, _NUM_HANDS)
#    print('Average margin ', margin/(2*_NUM_HANDS))
    wins, margin = play_games(player1, player2)
    print('Average wins {} margin {}'.format(wins, margin))
