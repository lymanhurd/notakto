
# NoTakTo
# An implementation of the game NoTakTo introduced in the paper:
# The Secrets of Notakto: Winning at X-only  Tic-Tac-Toe by Thane E. Plambeck,
# Greg Whitehead.
from bottle import default_app, route
from notakto import smart_move


@route('/move/<move_string>')
def computer_move(move_string):
    return smart_move(move_string)

application = default_app()
