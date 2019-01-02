#!/usr/bin/python2.7
"""Unit tests for cribbage.py."""

import logging
import unittest

from cribbage import cribbage_command


_SCORE_TESTING = (('5c,5d,5h,js', '5s', 29),
                  ('5c,5d,5h,ks', '5s', 28),
                  ('ac,7c,7d,7h', '7s', 24),
                  ('4c,4s,5d,5h', '6s', 24),
                  ('7c,7d,8d,9h', '8s', 24),
                  ('4c,5c,5d,6h', '5s', 23),
                  ('5c,5d,kd,kh', '5s', 22),
                 )


class TestCribbage(unittest.TestCase):

    def test_discard(self):
        query = {'hand': 'AH,3D,5C,JC,QC,KC'}
        self.assertEqual('AH,3D', cribbage_command('discard', query))

    def test_play(self):
        query = {'hand': 'ac,2d,4s,5c', 'comp_cards': '', 'human_cards': '0c', 'dealer':'h', 'start': 'Jd'}
        self.assertEqual('5C', cribbage_command('play', query))

    def test_score(self):
        query = {'hand1': '5c,jc,qc,kc', 'hand2': '5s,jd,qs,kd', 'crib':'ad,3c,4h,ks', 'start': '5d'}
        self.assertEqual({'hand1': 21, 'hand2': 18, 'crib': 7}, cribbage_command('score', query))
        for hand, start, score in _SCORE_TESTING:
            query = {'hand1': hand, 'start': start}
            self.assertEqual({'hand1': score}, cribbage_command('score', query))

    def test_sequence(self):
        query = {'seq': 'as,js,0s,5c,jd,5d'}
        self.assertEqual('2', cribbage_command('sequence', query))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
