"""Web app for hurd-sullivan.com."""

import logging

from bottle import default_app, hook, response, route, request, template
from notakto.notakto import smart_move
from cribbage.cribbage import cribbage_command
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

# Expected input (example): returns
# .../cribbage/discard?hand=0,1,2,3,4,5&comp_score=120&human_score=100&dealer=computer
# .../cribbage/discard?discard=0,1,2,3,4,5&comp_score=120&human_score=100
@route('/cribbage/<command>')
def handle_cribbage(command):
    """Cribbage commands."""
    return cribbage_command(command, request.query)


# Expected input (example): returns e.g., 0,1.
# .../cribbage/play?hand=0,1&comp_played=2,3&human_played=5,6,7&comp_score=120&human_score=100
# output 1
# @route('/cribbage/play')
# def cribbage_play():
#     """Return card to play."""
#     assert 0 <= int(request.query.comp_score) < 121 and 0 <= int(request.query.human_score) < 121
#     hand = request.query.hand.split(',')
#     comp_played = request.query.comp_played.split(',')
#     # human_played = [int(x) for x in ','.split(request.query.human_played)]
#     # assert len(hand) + len(comp_played) == 4
#     return hand[0].lower()

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

# @route('/forum')
# def display_forum():
#     forum_id = request.query.id
#     page = request.query.page or '1'
#     return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)

application = default_app()
