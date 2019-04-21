"""Unit tests for score.py."""

import logging
import unittest
from cribbage.deck import card_number
from cribbage.score import score, score_sequence

_SCORE_TESTING = (('5c,5d,5h,js', '5s', 29),
                  ('5c,5d,5h,ks', '5s', 28),
                  ('ac,7c,7d,7h', '7s', 24),
                  ('4c,4s,5d,5h', '6s', 24),
                  ('7c,7d,8d,9h', '8s', 24),
                  ('4c,5c,5d,6h', '5s', 23),
                  ('5c,5d,kd,kh', '5s', 22),
                  )


class TestCribbage(unittest.TestCase):
    def test_score(self):
        for hand_str, start_str, expected in _SCORE_TESTING:
            cards = [card_number(c) for c in hand_str.split(',')]
            start = card_number(start_str)
            self.assertEqual(score(cards, start, False), expected)

    def test_score_flush(self):
        cards = [card_number(c) for c in '5c,6c,qc,kc'.split(',')]
        start = card_number('3h')
        # if is_crib=False a flush of four cards is scored
        self.assertEqual(score(cards, start, False), 8)
        # if is_crib=False a flush of four cards is not scored
        self.assertEqual(score(cards, start, True), 4)
        # in either case a lush of five cards is scored
        self.assertEqual(score(cards, card_number('3c'), False), 9)
        self.assertEqual(score(cards, card_number('3c'), True), 9)

    def test_score_sequence_tuples(self):
        # first card doesn't score
        self.assertEqual(score_sequence([], card_number('3c')), 0)
        # score pair
        seq = [card_number(c) for c in 'ac,3h'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('3c')), 2)
        # score pair royal
        seq = [card_number(c) for c in 'ac,3h,3d'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('3c')), 6)
        # score double pair royal
        seq = [card_number(c) for c in 'ac,3h,3d,3s'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('3c')), 12)
        # score resets after 31 points
        seq = [card_number(c) for c in '7c,kc,kh,3h,3d,3s'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('3c')), 6)

    def test_score_sequence_runs(self):
        seq = [card_number(c) for c in 'ac,3c'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('2c')), 3)
        seq = [card_number(c) for c in '8c,ac,3c,6c,5c,4c'.split(',')]
        self.assertEqual(score_sequence(seq, card_number('2c')), 6)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
