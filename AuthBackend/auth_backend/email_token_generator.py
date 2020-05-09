import hashlib
import hmac
from datetime import date

from auth_backend import config
from auth_backend import settings

DEFAULT_KEY_SALT = '605be3c255d09593e8b3'
KEY_SALT = getattr(settings, 'KEY_SALT', DEFAULT_KEY_SALT)

DEFAULT_PASSWORD_RESET_TIMEOUT_DAYS = 2
PASSWORD_RESET_TIMEOUT_DAYS = getattr(
    settings, 'PASSWORD_RESET_TIMEOUT_DAYS', DEFAULT_PASSWORD_RESET_TIMEOUT_DAYS
)


def make_token(username, active_status):
    timestamp = make_timestamp()

    return make_token_with_timestamp(username, active_status, timestamp)


def make_timestamp():
    dt = date.today()
    return (dt - date(2001, 1, 1)).days


def make_token_with_timestamp(username, active_status, timestamp):
    try:
        ts_b36 = int_to_base36(timestamp)
    except ValueError as error:
        print(error)
    else:
        hash_string = salted_hmac(
            KEY_SALT,
            make_hash_value(username, active_status, timestamp),
            secret=config.PRIVATE_KEY,
        ).hexdigest()[::2]
        return f'{ts_b36}-{hash_string}'


def int_to_base36(i):
    char_set = '0123456789abcdefghijklmnopqrstuvwxyz'
    if i < 0:
        raise ValueError("Negative base36 conversion input.")
    if i < 36:
        return char_set[i]
    b36 = ''
    while i != 0:
        i, n = divmod(i, 36)
        b36 = char_set[n] + b36
    return b36


def salted_hmac(key_salt, value, secret=None):
    if not secret:
        secret = config.PRIVATE_KEY

    b_key_salt = str(key_salt).encode()
    b_secret = str(secret).encode()

    key = hashlib.sha1(b_key_salt + b_secret).digest()

    return hmac.new(key, msg=str(value).encode(), digestmod=hashlib.sha1)


def make_hash_value(username, active_status, timestamp):
    return str(username) + str(active_status) + str(timestamp)


def check_token(username, active_status, token):
    if not any((username, active_status, token)):
        return False

    try:
        ts_b36, _ = token.split("-")
    except ValueError:
        return False

    try:
        ts = base36_to_int(ts_b36)
    except ValueError:
        return False

    compared_token = make_token_with_timestamp(username, active_status, ts)

    if not hmac.compare_digest(compared_token.encode(), token.encode()):
        return False

    if (make_timestamp() - ts) > PASSWORD_RESET_TIMEOUT_DAYS:
        return False

    return True


def base36_to_int(s):
    if len(s) > 13:
        raise ValueError("Base36 input too large")
    return int(s, 36)
