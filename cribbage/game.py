"""Representation of a game between two players."""

import json
import logging
import threading

from cribbage.crib_player import create_player
from typing import Dict


class IllegalMoveException(Exception):
    pass


# Create a new game (need a lock to avoid duplicating ids).
def start_game(level: int = 1):
    with LOCK:
        game_id = max(GAME_DICT.keys()) + 1
        GAME_DICT[game_id] = Game(level, id)
    return game_id


def get_game(game_id: int):
    return GAME_DICT.get(game_id, None)


class Game(object):
    def __init__(self, level: int, game_id: int, is_dealer: bool = True):
        self.id = game_id
        self.player = create_player(0)
        self.opponent = create_player(level)

        # is_dealer is reversed on dealing the first hand
        self.player.is_dealer = not is_dealer
        self.opponent.is_dealer = not self.player.is_dealer

        self.start = None
        self.sequence = []
        self.hand_number = 0
        self.crib = []

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


# Dictionary containing all active games (to be replaced with a database).
# Maps from game_id to game object.
GAME_DICT: Dict[int, Game] = {}
LOCK = threading.Lock()

# TBD
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    pass
