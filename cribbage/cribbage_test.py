"""Unit tests for cribbage.py."""

import logging
import unittest
from cribbage.deck import card_number, Deck, DECK, hand_string, JACK, random_draw, seq_string, value


from cribbage.cribbage_commands import cribbage_command


class TestCribbage(unittest.TestCase):
    def test_start(self):
        hand_id, card_string = cribbage_command('start', {'is_dealer': 'True'})
        cards = [card_number(c) for c in card_string.split(',')]
        self.assertEqual(hand_id, 1)
        self.assertEqual(len(cards), 6)
        self.assertEqual(len(set(cards)), 6)

    def test_discard_non_dealer(self):
        hand_id, cards = cribbage_command('start', {'is_dealer': 'False'})
        discards = ','.join(cards.split(',')[:2])
        reply = cribbage_command('discard', {'id': hand_id, 'cards': discards})
        self.assertIsNone(reply)

    def test_play(self):
        hand_id, cards = cribbage_command('start', {'is_dealer': 'False'})
        to_play = cards.split(',')[0]
        logging.info('to_play %s', to_play)
        self.assertEqual('5C', cribbage_command('play', {'id': hand_id, 'card': to_play}))

    def test_crib_before_discard(self):
        hand_id, hand = cribbage_command('start', {'is_dealer': 'False'})
        # Cannot call "crib" before "discard".
        with self.assertRaises(AssertionError):
            cribbage_command('crib', {'id': hand_id})

    # def test_crib_after_discard(self):
    #     hand_id, cards = cribbage_command('start', {'is_dealer': 'False'})
    #     discards = ','.join(cards.split(',')[:2])
    #     cribbage_command('discard', {'cards': discards})
    #     crib = cribbage_command('crib', {'id': hand_id})
    #     self.assertEqual(len(crib.split(',')), 4)
    #     self.assertEqual(len(set(crib.split(','))), 4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
