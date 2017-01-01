
# NoTakTo
# An implementation of the game NoTakTo introduced in the paper:
# The Secrets of Notakto: Winning at X-only  Tic-Tac-Toe by Thane E. Plambeck,
# Greg Whitehead.
from bottle import default_app, route, static_file

@route('/move/<move_string>')
def computer_move(move_string):
    return notakto.smart_move(move_string)

application = default_app()
