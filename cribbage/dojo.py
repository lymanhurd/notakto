"""Framework for comparing two players."""
import logging

from cribbage.crib_player import create_player, GameOver, Player
from cribbage.crib_utils import DECK, hand_string, JACK, seq_count, seq_string, value
from cribbage.deck import Deck
from cribbage.score import score, score_sequence


NUM_GAMES = 1
NUM_HANDS = 5


def play_games(player1: Player, player2: Player, num_games: int = 1, alternate_start: bool = True) -> None:
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


def play_hands(player1: Player, player2: Player, num_hands: int) -> int:
    # The stronger player is assumed to go second so we record wins/margin
    # from Player 2's point of view.

    # Play games twice once from each side.
    margin = 0
    for i in range(num_hands):
        print('Player 1(%s) Player 2 (%s) Hand %d' % (player1.name, player2.name, i + 1))
        # reset players, hands and score
        deck = Deck()
        player1.score, player2.score = 0, 0
        first_hand = deck.deal(6)
        second_hand = deck.deal(6)
        start = deck.deal(1)[0]

        # Play hand with player2 as dealer.
        player1.start, player1.hand = start, first_hand[:]
        player2.start, player2.hand = start, second_hand[:]
        play_hand(player2, player1, start)

        # Play hand with player1 as dealer.
        player1.hand, player1.discarded = second_hand[:], []
        player2.hand, player2.discarded = first_hand[:], []
        play_hand(player1, player2, start)
        margin += player2.score - player1.score
        if i % 100 == 100:
            logging.warning('Hand %d current margin %d', i, margin)
    return margin


def play_game(first: Player, second: Player) -> bool:
    first.score = 0
    second.score = 0
    dealer, pone = first, second
    deck = Deck()
    hand = 1
    print('DEALER(%s) PONE(%s) Hand %d' % (dealer.name, dealer.score, hand))
    try:
        while first.score < 121 and second.score < 121:
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
    return first.score > second.score


def play_hand(dealer: Player, pone: Player, start: int) -> None:
    try:
        dealer.is_dealer = True
        pone.is_dealer = False
        dealer_discard = dealer.discard()
        pone_discard = pone.discard()
        if value(start) == JACK:  # his heels
            dealer.add(2, verbose=False)
            print('Start card: %s %s +2 (%d) (for his heels)' % (DECK[start], dealer.score, dealer.name))
        else:
            print('Start card: %s' % DECK[start])
        pegging(dealer, pone)

        sc = score(pone.hand, start)
        pone.add(sc, verbose=False)
        print('pone   [%s] start %s score %d (%d)' % (hand_string(pone.hand), DECK[start], sc, pone.score))

        sc = score(dealer.hand, start)
        dealer.add(sc, verbose=False)
        print('dealer [%s] start %s score %d (%d)' % (hand_string(dealer.hand), DECK[start], sc, dealer.score))

        crib = dealer_discard + pone_discard
        sc = score(crib, start, is_crib=True)
        dealer.add(sc, verbose=False)
        print('crib   [%s] start %s score %d (%d)' % (hand_string(crib), DECK[start], sc, dealer.score))
        print('DEALER(%s) %d PONE(%s) %d\n' % (dealer.name, dealer.score, pone.name, pone.score))
    except GameOver:
        return


def pegging(dealer: Player, pone: Player) -> None:
    seq = []
    cards_played = 0
    while cards_played < 8:
        for player, opponent in ((pone, dealer), (dealer, pone)):
            card, go = player.next_card(seq)
            opponent.opponent_passed = go
            if go:
                print('%s says go [%s]' % (player.name, seq_string(seq)))
                if opponent.passed:
                    # Score one for "last card" unless last card scored for 31.
                    if seq_count(seq) > 0:
                        print('%s last card' % player.name)
                        player.add(1)
            else:
                card_score = score_sequence(seq, card)
                seq.append(card)
                player.add(card_score, verbose=False)
                print('%s plays %s [%s] + %d (%d)' % (player.name, DECK[card], seq_string(seq),
                                                      card_score, player.score))
                cards_played += 1
                if cards_played == 8:
                    print('%s + 1 last (8th) card' % player.name)
                    player.add(1)
                    break


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    score_sequence([20, 32, 42, 21, 25], 26)
    p1 = create_player(level=0)
    p2 = create_player(level=2)
    m = play_hands(p1, p2, NUM_HANDS)
    print('Average margin ', m / (2 * NUM_HANDS))
    # play_games(player1, player2, NUM_GAMES)
    # assert NUM_GAMES == player1.wins + player2.wins
    # print('Player2 winning percentage {}'.format(100 * (player2.wins - player1.wins)/NUM_GAMES))
