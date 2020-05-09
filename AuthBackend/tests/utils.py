from faker import Faker

from auth_backend import token_validation
from auth_backend.email_token_generator import make_token
from auth_backend.models import UserModel
from auth_backend.utils import urlsafe_base64_encode
from tests.constants import PRIVATE_KEY

fake = Faker()
#
#
# def create_login_user(bad_email=False, has_email=False):
#     new_user = {
#         'username': fake.first_name(),
#         'password': fake.password(length=15, special_chars=True),
#     }
#
#     if has_email:
#         email = '' if bad_email else fake.free_email()
#         new_user.update({'email': email})
#
#     return new_user


def create_login_user():
    return {
        'username': fake.first_name(),
        'password': fake.password(length=15, special_chars=True),
    }


def create_register_user(bad_email=False, bad_password_2=False):
    new_user = create_login_user()

    new_user.update({
        'email': '' if bad_email else fake.free_email(),
        'password2': fake.password() if bad_password_2 else new_user['password']
    })

    return new_user


def get_login_user_from_register_user(register_user):
    login_user = register_user.copy()
    login_user.pop('email')
    login_user.pop('password2')

    return login_user


def register_user(client, bad_email=False, bad_password_2=False):
    new_user = create_register_user(bad_email, bad_password_2)

    response = client.post('/api/auth/register/', data=new_user)

    return response, new_user


def activate_user(client, username, bad_uname64=False, bad_token=False):
    if bad_uname64:
        unameb64 = fake.pystr()
    else:
        b_uname = str(username).encode()
        unameb64 = urlsafe_base64_encode(b_uname)

    token = fake.pystr() if bad_token else make_token(username, False)

    return client.post(f'/api/auth/activate/{unameb64}/{token}/')


def delete_user(client, user_data, bad_password=False):
    username = user_data['username']
    user = UserModel.query.filter_by(name=username).first()

    user_id = user.id if user else 123456

    headers = get_headers(username, user_id)
    data = {
        'password': fake.password() if bad_password else user_data['password']
    }

    return client.delete(f'/api/auth/{user_id}/', headers=headers, data=data)


def get_headers(username, user_id):
    header = token_validation.generate_token_header(
        username, user_id, PRIVATE_KEY
    )

    return {
        'Authorization': header,
    }
