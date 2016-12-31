
# NoTakTo
# An implementation of the game NoTakTo introduced in the paper:
# The Secrets of Notakto: Winning at X-only  Tic-Tac-Toe by Thane E. Plambeck,
# Greg Whitehead.
from bottle import default_app, route, static_file
from random import randint

@route('/move/<move_string>')
def compute_move(move_string):
    d = {}
    l = len(move_string)
    n = randint(0, l - 1)
    for i in range(l):
      j = (i + n) % l
      if move_string[j] == '-':  
        d['board'] = j / 9
        d['column'] = j % 3
        d['row'] = (j % 9) / 3
        break;
    return d

application = default_app()

