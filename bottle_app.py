"""Web app for hurd-sullivan.com."""

from bottle import default_app, route
from notakto.notakto import smart_move
from checkers.tree_search import find_move

# NoTakTo
# An implementation of the game NoTakTo introduced in the paper:
# The Secrets of Notakto: Winning at X-only  Tic-Tac-Toe by Thane E. Plambeck,
# Greg Whitehead.
@route('/notakto/move/<move_string>')
def computer_move(move_string):
    """Return move for NoTakTo."""
    return smart_move(move_string)


# Checkers
# A simplistic checkers AI by Lyman Hurd.  Expects a 32 character string.  This
# endpoint means it is black's move.
@route('/checkers/black/<move_string>')
def computer_move(move_string):
    """Return move for checkers."""
    return find_move(move_string, True)

# Checkers
# A simplistic checkers AI by Lyman Hurd.  Expects a 32 character string with
# the first character being the player whose move it is.  This
# endpoint means it is red's move.
@route('/checkers/red/<move_string>')
def computer_move(move_string):
    """Return move for checkers."""
    return find_move(move_string, False)


application = default_app()
