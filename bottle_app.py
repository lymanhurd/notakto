"""Web app for hurd-sullivan.com."""

from bottle import default_app, hook, response, route, request, template
from notakto.notakto import smart_move
# from checkers_ai.tree_search import find_move

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = (
        'glennqhurd.pythonanywhere.com')

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
#@route('/checkers/black/<move_string>')
#def black_computer_move(move_string):
#    """Return move for checkers."""
#    return find_move(move_string, True)

# Checkers
# A simplistic checkers AI by Lyman Hurd.  Expects a 32 character string with
# the first character being the player whose move it is.  This
# endpoint means it is red's move.
#@route('/checkers/red/<move_string>')
#def red_computer_move(move_string):
#    """Return move for checkers."""
#    return find_move(move_string, False)

@route('/forum')
def display_forum():
    forum_id = request.query.id
    page = request.query.page or '1'
    return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)

application = default_app()
