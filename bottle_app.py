"""Web app for hurd-sullivan.com."""

# import logging

from bottle import default_app, hook, response, route, request
from cribbage.cribbage import cribbage_command

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return


# Handler for cribbage commands.
@route('/cribbage/<command>')
def handle_cribbage(command):
    """Handler for cribbage commands."""
    return cribbage_command(command, request.query)

application = default_app()
