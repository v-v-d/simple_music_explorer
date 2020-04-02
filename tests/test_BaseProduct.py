from pytest import fixture, raises

from models.base import BaseProduct
from models.exceptions import WrongInstanceError
from models.users import Artist


@fixture()
def artist_name_fixture():
    return 'Homer'


@fixture()
def email_fixture():
    return 'homer@mail.com'


@fixture()
def price_fixture():
    return 100


@fixture()
def product_type_fixture():
    return 'Album'


@fixture()
def artist_fixture(artist_name_fixture, email_fixture):
    return Artist(artist_name_fixture, email_fixture)


@fixture()
def album_name_fixture(artist_name_fixture, email_fixture):
    return 'Test'


@fixture()
def base_product_fixture(album_name_fixture, artist_fixture, price_fixture, product_type_fixture):
    return BaseProduct(album_name_fixture, artist_fixture, price_fixture, product_type_fixture)


@fixture()
def invalid_base_product_fixture():
    return 'invalid instance'


def test_base_product_init(
        base_product_fixture, album_name_fixture, artist_fixture,
        price_fixture, product_type_fixture
):
    assert all((
        base_product_fixture.name == album_name_fixture,
        base_product_fixture.artist == artist_fixture,
        base_product_fixture.price == price_fixture,
        base_product_fixture.product_type == product_type_fixture
    ))


def test_base_product_str(base_product_fixture, album_name_fixture):
    assert str(base_product_fixture) == album_name_fixture


def test_base_product_eq(
        base_product_fixture, album_name_fixture, artist_fixture,
        price_fixture, product_type_fixture
):
    base_product = BaseProduct(album_name_fixture, artist_fixture, price_fixture, product_type_fixture)
    assert base_product_fixture == base_product


def test_base_product_eq_invalid(base_product_fixture, invalid_base_product_fixture):
    with raises(WrongInstanceError):
        assert base_product_fixture == invalid_base_product_fixture
