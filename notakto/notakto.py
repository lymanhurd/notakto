from monoid import is_winning
from random import randint

import logging


DEAD_CONFIGURATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ]


def first_move(board_string, criterion):
  """Return a random move satisfying the criterion.
  """
  d = {}
  l = len(board_string)
  n = randint(0, l - 1)
  for i in range(l):
    j = (i + n) % l
    if board_string[j] == '-' and criterion(board_string, j):
      d['board'] = j / 9
      d['column'] = j % 3
      d['row'] = (j % 9) / 3
      return d;


def smart_move(board_string):
  """Return an optimal move if one exists.

  Picks a random winning move if possible, and if not tries to make a move that
  doesn't kill a board and otherwise it makes a random move.
  """
  winning_move = first_move(board_string, move_wins)
  if winning_move:
    logging.info("Found winning move.")
    return winning_move
  else:
    logging.info("Random move.")
    return first_move(board_string, lambda b,i: b[i] == '-')


def move_wins(board_string, index):
  board_string = board_string.upper()
  l = list(board_string)
  l[index] = 'X'
  board_list = list(map(''.join, zip(*[iter(''.join(l))]*9)))
  return is_winning(board_list)


def is_dead(board):
  logging.info("board %s" % board)
  for config in DEAD_CONFIGURATIONS:
    if (board[config[0]] != '-' and board[config[1]] != '-' and
        board[config[2]] != '-'):
      return True
  return False