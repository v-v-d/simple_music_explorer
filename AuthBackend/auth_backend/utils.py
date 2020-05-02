from flask_restplus import abort

from auth_backend import config
from auth_backend.token_validation import validate_token_header


def authentication_header_parser(value):
    user = validate_token_header(value, config.PUBLIC_KEY)
    if not user:
        abort(401)

    return user
