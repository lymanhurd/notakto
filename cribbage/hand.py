from __future__ import annotations

from cribbage.crib_player import StandardPlusPlayer
from cribbage.deck import card_number, Deck, hand_string
from typing import Optional

import logging


class Hand(object):
    default_hand = None

    def __init__(self, is_dealer: bool = False):
        self.is_dealer = is_dealer
        self.id = 1
        deck = Deck()
        self.player_cards = deck.deal(6)
        self.computer_cards = deck.deal(6)
        self.start = deck.deal(1)[0]
        self.crib = []
        self.seq = []
        self.opponent = StandardPlusPlayer()

    @classmethod
    def create_hand(cls, is_dealer) -> Hand:
        cls.default_hand = cls(is_dealer)
        return cls.default_hand

    @classmethod
    def get_hand_by_id(cls, hand_id) -> Hand:
        del hand_id
        if not cls.default_hand:
            cls.create_hand(True)
        return cls.default_hand

    def discard(self, card_string: str) -> Optional[str]:
        assert len(self.crib) == 0
        assert len(self.player_cards) == 6 and len(self.computer_cards) == 6
        cards = [card_number(c) for c in card_string.split(',') if c]
        self.crib = cards
        self.crib += self.opponent.choose_discards(self.is_dealer, self.computer_cards)
        logging.info('crib = %s', self.crib)
        if self.is_dealer:
            return self.opponent.next_card(self.computer_cards, self.seq, self.start)

    def play(self, card_str: str) -> str:
        card = card_number(card_str)
        self.seq.append(card)
        if len(self.seq) < 8:
            return self.opponent.next_card(self.computer_cards, self.seq, self.start)

    def crib_string(self) -> str:
        assert len(self.seq) == 8 and len(self.crib) == 4
        return hand_string(self.crib, ',')

    def player_cards_string(self) -> str:
        return hand_string(self.player_cards, ',')
