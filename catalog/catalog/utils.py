from flask_restplus import abort

from catalog import config
from catalog.token import validate_token_header


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username
