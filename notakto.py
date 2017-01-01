from monoid import is_winning
from random import randint


def first_move(board_string, criterion):
  """Return a random move satisfying the criterion.
  """
  d = {}
  l = len(board_string)
  n = randint(0, l - 1)
  for i in range(l):
    j = (i + n) % l
    if criterion(board_string, j):
      d['board'] = j / 9
      d['column'] = j % 3
      d['row'] = (j % 9) / 3
      return d;


def smart_move(board_string):
  """Return an optimal move if one exists and otherwise a random one.
  """
  def move_wins(board_string, index):
    if board_string[index] == '-':
      board_string = board_string.upper()
      l = list(board_string)
      l[index] = 'X'
      board_list = list(map(''.join, zip(*[iter(''.join(l))]*9)))
      return is_winning(board_list)
    else:
      return False
  winning_move = first_move(board_string, move_wins)
  if winning_move:
    return winning_move
  else:
    return first_move(board_string, lambda b,i: b[i] == '-')
