from __future__ import annotations

from cribbage.crib_player import StandardPlusPlayer
from cribbage.deck import card_number, Deck, DECK, hand_string, JACK, random_draw, seq_string, value
from typing import Optional


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
    def create_hand(cls) -> Hand:
        cls.default_hand = cls()
        return cls.default_hand

    @classmethod
    def get_hand_by_id(cls, hand_id) -> Hand:
        del hand_id
        return cls.default_hand

    def discard(self, card_string: str) -> Optional[str]:
        assert len(self.crib) == 0
        assert len(self.player_cards) == 6 and self.computer_cards == 6
        cards = [card_number(c) for c in card_string.split(',') if c]
        self.crib = cards
        self.crib += self.opponent.discard(self.computer_cards)
        if self.is_dealer():
            return self.opponent.next_card(self.computer_cards, self.seq, self.start)

    def play(self, card) -> str:
        card = card_number(query.get('play', ''))
        self.seq += card
        if len(self.seq) < 8:
            return self.opponent.next_card(self.computer_cards, self.seq, self.start)

    def crib(self) -> str:
        assert len(self.seq) == 8 and len(self.crib) == 4
        return hand_string(self.crib)
