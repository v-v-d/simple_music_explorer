from pytest import fixture

from models.users import User


@fixture()
def user_name_fixture():
    return 'Homer'


@fixture()
def last_name_fixture():
    return 'Simpson'


@fixture()
def email_fixture():
    return 'homer@mail.com'


@fixture()
def user_fixture(user_name_fixture, email_fixture, last_name_fixture):
    return User(user_name_fixture, email_fixture, last_name_fixture)


def test_user_init(
        user_fixture, user_name_fixture,
        last_name_fixture, email_fixture
):
    assert all((
        user_fixture.name == user_name_fixture,
        user_fixture.last_name == last_name_fixture,
        user_fixture.email == email_fixture,
    ))


def test_user_get_full_name(user_fixture, user_name_fixture, last_name_fixture):
    assert user_fixture.get_full_name() == f'{user_name_fixture} {last_name_fixture}'
