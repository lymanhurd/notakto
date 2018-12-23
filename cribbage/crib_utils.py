"""Helper routines for interfacing between web app and AI."""

SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 10)] + ['0', 'J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]


def card_number(name):
    return -1 if not name else DECK.index(name[-2:].upper()) # map "10H" to "0H" for example.


def card_value(card):
    return min(10, 1 + card % 13)


def merge(comp_cards, human_cards, computer_dealt):
    first = comp_cards if computer_dealt else human_cards
    second = human_cards if computer_dealt else comp_cards
    count = 0
    merged = []
    first_pass, second_pass = False, False
    while len(first) + len(second) > 0:
        if first and card_value(first[0]) + count <= 31:
            merged.append(first[0])
            count += card_value(first.pop(0))
        else:
            first_pass = True
            if second_pass:
                count = card_value(first[0])
                merged = [first.pop(0)]
                first_pass, second_pass = False, False
        if second and card_value(second[0]) + count <= 31:
            merged.append(second[0])
            count += card_value(second.pop(0))
        else:
            second_pass = True
            if first_pass:
                count = card_value(second[0])
                merged = [second.pop(0)]
                first_pass, second_pass = False, False
    return merged, count
