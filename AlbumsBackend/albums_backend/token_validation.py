import logging
from datetime import datetime, timedelta

import jwt
from parse import parse

logger = logging.getLogger(__name__)


def encode_token(payload, private_key):
    return jwt.encode(payload, private_key, algorithm='RS256')


def decode_token(token, public_key):
    return jwt.decode(token, public_key, algoritms='RS256')


def generate_token_header(username, user_id, private_key):
    """
    Generate a token header base on the user info. Sign using the private key.
    """
    payload = {
        'user': {
            'name': username,
            'id': user_id,
        },
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=2),
    }
    token = encode_token(payload, private_key)
    token = token.decode('utf8')
    return f'Bearer {token}'


def validate_token_header(header, public_key):
    """
    Validate that a token header is correct

    If correct, it return the username, if not, it
    returns None
    """
    if not header:
        logger.info('No header')
        return None

    # Retrieve the Bearer token
    parse_result = parse('Bearer {}', header)
    if not parse_result:
        logger.info(f'Wrong format for header "{header}"')
        return None

    token = parse_result[0]

    try:
        decoded_token = decode_token(token.encode('utf8'), public_key)
    except jwt.exceptions.DecodeError:
        logger.warning(f'Error decoding header "{header}". '
                       'This may be key missmatch or wrong key')
        return None
    except jwt.exceptions.ExpiredSignatureError:
        logger.error(f'Authentication header has expired')
        return None

    if not is_dict_keys_valid(('exp', 'user'), decoded_token, 'decoded_token'):
        return None

    user = decoded_token['user']
    if not isinstance(user, dict):
        logger.warning(f'Wrong user type. Expected: dict, got: {type(user)}')
        return None

    if not is_dict_keys_valid(('name', 'id'), user, 'user'):
        return None

    logger.info('Header successfully validated')
    return user


def is_dict_keys_valid(expected_keys, dict_obj, obj_name):
    if not all(key in dict_obj for key in expected_keys):
        logger.warning(
            f'Wrong {obj_name} keys in token. '
            f'Expected: {", ".join(expected_keys)}, '
            f'got: {", ".join(dict_obj.keys())}'
        )
        return False
    return True
