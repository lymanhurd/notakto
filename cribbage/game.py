"""Representation of a game between two players."""

import json
import logging
import threading

from cribbage.crib_player import create_player, GameOver
from cribbage.crib_utils import card_number, card_points, DECK, hand_string, seq_count
from cribbage.deck import Deck
from cribbage.score import score, score_sequence


class IllegalMoveException(Exception):
    pass


# Dictionary containing all active games (to be replaced with a database).
# Maps from game_id to game object.
GAME_DICT = {0: None}
LOCK = threading.Lock()


# Create a new game (need a lock to avoid duplicating ids).
def start_game(level=-1):
    with LOCK:
        game_id = max(GAME_DICT.keys()) + 1
        GAME_DICT[game_id] = Game(level, id)
    return game_id


def get_game(id):
    return GAME_DICT.get(id, None)


class Game(object):
    def __init__(self, level, id, is_dealer=True):
        self.id = id
        self.player = create_player(0)
        self.opponent = create_player(level)

        # is_dealer is reversed on dealing the first hand
        self.player.is_dealer = not is_dealer
        self.opponent.is_dealer = not self.player.is_dealer

        self.start = None
        self.sequence = []
        self.hand_number = 0
        self.crib = []

    def game_over(self) -> bool:
        return self.player.score > 120 or self.opponent.score > 120

    def new_hand(self) -> None:
        assert not self.game_over()
        self.hand_number += 1
        self.sequence = []
        deck = Deck()
        self.player.hand = deck.deal(6)
        self.opponent.hand = deck.deal(6)
        self.start = deck.deal(1)[0]
        # swap dealer
        self.player.is_dealer = not self.player.is_dealer
        self.opponent.is_dealer = not self.opponent.is_dealer

    def end_of_hand(self) -> None:
        logging.info('End of hand.')
        assert not self.game_over()
        self.crib = self.player.discarded + self.opponent.discarded
        if self.player.is_dealer:
            pone, dealer = self.opponent, self.player
        else:
            dealer, pone = self.player, self.opponent
        try:
            # score in order pone, dealer, crib
            pone.add(score(pone.hand, self.start))
            dealer.add(score(dealer.hand, self.start))
            dealer.add(score(self.crib, self.start, is_crib=True))
        except GameOver:
            return
        self.new_hand()

    def discard(self, cards) -> None:
        assert not self.game_over()
        if len(self.player.hand) != 6:
            raise IllegalMoveException('Game is not in the discard phase')
        if (len(cards) != 2 or len(set(cards)) != 2 or
                cards[0] not in self.player.hand or
                cards[1] not in self.player.hand):
            raise IllegalMoveException('Need to discard two cards from hand')
        self.player.discarded = cards
        self.player.hand.remove(cards[0])
        self.player.hand.remove(cards[1])
        self.opponent.discard()

    def play_card(self, card) -> None:
        assert not self.game_over()        
        # check for legality
        if len(self.player.hand) != 4 or self.game_over():
            raise IllegalMoveException('Game is not in the play phase')
        if card not in self.player.hand:
            raise IllegalMoveException('Need to play a card from hand')
        cur_count = seq_count(self.sequence)
        if cur_count + card_points(card) > 31:
            raise IllegalMoveException('Illegal card %s' % DECK[card])

        # add card to sequence and score it
        try:
            self.player.add(score_sequence(self.sequence, card))
            self.sequence.append(card)
        except GameOver:
            return

        # make computer's move
        last_move = False
        try:
            while len(self.sequence) < 8:
                card, go = self.opponent.next_card(self.sequence)
                cardscore = score_sequence(self.sequence, card)
                self.sequence.append(card)
                self.opponent.add(cardscore)
                if not self.player.must_pass(self.sequence):
                    return
                if go:
                    if last_move:
                        self.opponent.add(1)
                        return
                    else:
                        last_move = True
        except GameOver:
            return
        # if we get this far, the hand is over.
        self.end_of_hand()

    # express game statistics as a string
    def game_object(self):
        d = {}
        d['id'] = self.id
        d['is_dealer'] = self.player.is_dealer
        d['hand_number'] = self.hand_number        
        d['name'] = [self.player.name, self.opponent.name]
        d['score'] = [self.player.score, self.opponent.score]
        d['hand'] = self.player.hand
        d['sequence'] = self.sequence
        if self.crib:
            d['crib'] = self.crib
        return json.dumps(d)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    id = start_game()
    game = get_game(id)
    game.new_hand()
    print(hand_string(sorted(game.player.hand)))
    d = input('Choose discards: ')
    discards = [card_number(c) for c in d.split()]
    game.discard(discards)
    while not game.game_over():
        print(hand_string(sorted([c for c in game.player.hand if c not in game.sequence])))
        d = input('Choose card to play: ')
        game.play_card(card_number(d))
        print('Sequence: %s' % hand_string(game.sequence))
        print('Scores (player %d computer %d)' % (game.player.score,
                                                  game.opponent.score))
