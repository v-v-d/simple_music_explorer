import base64
import hmac

from flask_mail import Mail, Message
from flask_restplus import abort

from auth_backend import config
from auth_backend.email_token_generator import make_token
from auth_backend.token_validation import validate_token_header

mail = Mail()


def authentication_header_parser(value):
    user = validate_token_header(value, config.PUBLIC_KEY)
    if not user:
        abort(401)

    return user


def get_password_digest(password):
    hmac_obj = hmac.new(
        config.PRIVATE_KEY.encode(), password.encode(),
        digestmod='sha256'
    )
    return hmac_obj.hexdigest()


def send_verify_email(recipient, url_root, domain, username, active_status):
    b_username = str(username).encode()
    uname = urlsafe_base64_encode(b_username)
    token = make_token(username, active_status)

    subject = f"Please activate your account on {domain}"
    url = f'{url_root}api/auth/activate/{uname}/{token}/'
    message = f"Follow the link below to complete the register:\n{url}"

    with mail.record_messages() as outbox:
        try:
            mail.send_message(
                subject=subject, body=message, recipients=[recipient]
            )
        except Exception as error:
            print(error)
        else:
            return len(outbox)


def urlsafe_base64_encode(b_str):
    return base64.urlsafe_b64encode(b_str).rstrip(b'\n=').decode('ascii')


def urlsafe_base64_decode(s):
    s = s.encode()
    try:
        return base64.urlsafe_b64decode(s.ljust(len(s) + len(s) % 4, b'='))
    except Exception as error:
        raise ValueError(error)


def is_password_valid(user, password):
    password_digest = get_password_digest(password)

    return hmac.compare_digest(password_digest.encode(), user.password.encode())
