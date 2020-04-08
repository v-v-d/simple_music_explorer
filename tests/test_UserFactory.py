from pytest import fixture

from models_.users import UserFactory, User


@fixture()
def user_cls_type_fixture():
    return 'User'


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


def test_user_factory(
        user_fixture, user_name_fixture, email_fixture,
        last_name_fixture, user_cls_type_fixture
):
    user = UserFactory.create_user(
        user_cls_type_fixture, user_name_fixture,
        email_fixture, last_name=last_name_fixture
    )
    assert all((
        user_fixture.name == user.name,
        user_fixture.last_name == user.last_name,
        user_fixture.email == user.email,
        user_fixture.is_active == user.is_active,
    ))
