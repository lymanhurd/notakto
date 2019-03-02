"""Framework for comparing two players."""

from __future__ import division
from __future__ import print_function

import logging

from crib_player import create_player, GameOver
from crib_utils import DECK, hand_string, seq_count
from deck import Deck
from score import score, score_sequence


NUM_GAMES = 1
NUM_HANDS = 500


def play_games(player1, player2, num_games=1, alternate_start=True):
    first, second = player1, player2
    for i in range(num_games):
        logging.debug('Game %d', i)
        first_won = play_game(first, second)
        if first_won:
            logging.debug('Player %s won', first.name)
            logging.debug('%s %d %s %d', first.name, first.score, second.name, second.score)
            first, second = second, first
        else:
            logging.debug('Player %s won', second.name)
            logging.debug('%s %d %s %d', first.name, first.score, second.name, second.score)
            if not alternate_start:
                first, second = second, first


def play_hands(player1, player2, num_hands):
    # The strongerplayer is assumed to go second so we record wins/margin
    # from Player 2's point of view.

    # Play games twice once from each side.
    margin = 0
    for i in range(num_hands):
        # reset players, hands and score
        deck = Deck()
        player1.score, player2.score = 0, 0
        first_hand = deck.deal(6)
        second_hand = deck.deal(6)
        start = deck.deal(1)[0]

        # Play hands with player2 as dealer.        
        player1.start, player1.hand = start, first_hand
        player2.start, player2.hand = start, second_hand
        play_hand(player2, player1, start)
        logging.info('Hand %d Player1 %d Player2 %d', i, player1.score, player2.score)

        # Play hands with player1 as dealer.
        player1.hand = second_hand
        player2.hand = first_hand
        play_hand(player1, player2, start)
        logging.info('Hand %d Player1 %d Player2 %d', i, player1.score, player2.score)

        margin += player2.score - player1.score
        logging.info('current margin %d', margin)
    return margin


def play_game(first, second):
    first.score = 0
    second.score = 0
    dealer, pone = first, second
    deck = Deck()
    hand = 1
    try:
        while first.score < 121 and second.score < 121:
            logging.debug('Hand %d', hand)
            deck.shuffle()
            dealer.hand = deck.deal(6)
            pone.hand = deck.deal(6)
            start = deck.deal(1)[0]
            dealer.start = start
            pone.start = start
            play_hand(dealer, pone, start)
            dealer, pone = pone, dealer
            hand += 1
    except GameOver:
        if first.score > second.score:
            first.wins += 1
        else:
            second.wins += 1


def play_hand(dealer, pone, start):
    logging.debug('Dealer %s %d Pone %s %d', dealer.name, dealer.score,
                 pone.name, pone.score)
    logging.debug('Start card: %s', DECK[start])
    if start % 13 == 10:  # his heels
        dealer.add(2)

    dcrib = dealer.discard(True, pone.score)
    logging.debug('dealer hand %s discard %s', hand_string(dealer.hand), hand_string(dcrib))

    pcrib  = pone.discard(False, dealer.score)
    logging.debug('pone   hand %s discard %s', hand_string(pone.hand), hand_string(pcrib))    

    pegging(dealer, pone, start)

    logging.debug('%s %d %s %d', dealer.name, dealer.score, pone.name, pone.score)
    sc = score(pone.hand, start)
    logging.debug('pone   hand %s start %s score %d', hand_string(pone.hand), DECK[start], sc)
    pone.add(sc)

    sc = score(dealer.hand, start)
    logging.debug('dealer hand %s start %s score %d', hand_string(dealer.hand), DECK[start], sc)
    dealer.add(sc)

    crib = dcrib + pcrib
    sc = score(crib, start, is_crib=True)
    logging.debug('crib   hand %s start %s score %d', hand_string(crib), DECK[start], sc)
    dealer.add(sc)

    logging.debug('DEALER(%s) %d PONE(%s) %d\n', dealer.name, dealer.score, pone.name, pone.score)    


def pegging(dealer, pone, start):
    seq = []
    cards_played = 0
    go = True
    cur_count = 0
    while cards_played < 8:
        for player, opponent in ((pone, dealer), (dealer, pone)):
            card, go = player.next_card(seq, cur_count)
            
            if go:
                logging.debug('%s says go', player.name)
                if opponent.passed:
                    # Score one for "last card" unless last card scored for 31.
                    if cur_count > 0:
                        logging.debug('%s + 1 last card', player.name)
                        player.add(1)
                        cur_count = 0
            else:
                cardscore = score_sequence(seq, card)
                seq.append(card)
                cur_count = seq_count(seq)
                logging.debug('%s %s score=%d cur_count=%d', player.name,
                             DECK[card], cardscore, cur_count)
                player.add(cardscore)
                cards_played += 1
                if cards_played == 8:
                    logging.debug('%s + 1 last (8th) card', player.name)
                    player.add(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    player1 = create_player(level=1, name='level1')
    player2 = create_player(level=2, name='level2')
    margin = play_hands(player1, player2, NUM_HANDS)
    print('Average margin ', margin/(2*NUM_HANDS))
    # play_games(player1, player2, NUM_GAMES)
    # assert NUM_GAMES == player1.wins + player2.wins
    # print('Player2 winning percentage {}'.format(100 * (player2.wins - player1.wins)/NUM_GAMES))
