"""Class representing a deck of cards."""

class Deck():

    def __init__(self):
        random.seed('deterministic')
        self.cards = range(52)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n):
        cards = self.deck[:n]
        del self.deck[:n]
        return cards
