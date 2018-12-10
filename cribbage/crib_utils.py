import logging


SUITS = ['C', 'D', 'H', 'S']
CARD_NAMES = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
DECK = [n + s for s in SUITS for n in CARD_NAMES]


def card_number(name):
    if name[0] == '0':
        name = '1' + name
    return DECK.index(name.upper())


def card_value(card):
    return min(10, 1 + card % 13)


def merge(first, second):
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
    return merged
