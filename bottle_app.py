"""Web app for hurd-sullivan.com."""

from bottle import default_app, route
from notakto.notakto import smart_move


# NoTakTo
# An implementation of the game NoTakTo introduced in the paper:
# The Secrets of Notakto: Winning at X-only  Tic-Tac-Toe by Thane E. Plambeck,
# Greg Whitehead.
@route('/notakto/move/<move_string>')
def computer_move(move_string):
    """Return ove for NoTakTo."""
    return smart_move(move_string)


application = default_app()
