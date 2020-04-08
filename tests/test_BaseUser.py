from pytest import fixture, raises

from models_.base import BaseUser
from models_.exceptions import WrongInstanceError


@fixture()
def artist_name_fixture():
    return 'Homer'


@fixture()
def email_fixture():
    return 'homer@mail.com'


@fixture()
def base_user_fixture(artist_name_fixture, email_fixture):
    return BaseUser(artist_name_fixture, email_fixture)


@fixture()
def invalid_base_user_fixture():
    return 'invalid instance'


def test_base_user_init(base_user_fixture, artist_name_fixture, email_fixture):
    assert all((
        base_user_fixture.name == artist_name_fixture,
        base_user_fixture.email == email_fixture,
        base_user_fixture.is_active
    ))


def test_base_user_str(base_user_fixture, artist_name_fixture):
    assert str(base_user_fixture) == artist_name_fixture


def test_base_user_eq(base_user_fixture, artist_name_fixture, email_fixture):
    base_user = BaseUser(artist_name_fixture, email_fixture)
    assert base_user_fixture == base_user


def test_base_user_eq_invalid(base_user_fixture, invalid_base_user_fixture):
    with raises(WrongInstanceError):
        assert base_user_fixture == invalid_base_user_fixture
