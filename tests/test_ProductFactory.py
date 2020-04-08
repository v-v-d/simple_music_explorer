from datetime import datetime

from pytest import fixture

from models_.products import Song, Album, ProductFactory
from models_.users import Artist


@fixture()
def product_cls_type_fixture():
    return 'Song'


@fixture()
def name_fixture():
    return 'Test'


@fixture()
def artist_fixture():
    return Artist('test', 'test@test.com')


@fixture()
def price_fixture():
    return 100


@fixture()
def product_type_fixture():
    return 'Song'


@fixture()
def album_fixture():
    return Album(
        'test', artist_fixture, 100, 'Album',
        'LP', 'test', datetime.now()
    )


@fixture()
def song_fixture(
        name_fixture, artist_fixture, price_fixture,
        product_type_fixture, album_fixture
):
    return Song(
        name_fixture, artist_fixture, price_fixture,
        product_type_fixture, album_fixture
    )


def test_product_factory(
        product_cls_type_fixture, name_fixture, artist_fixture,
        price_fixture, product_type_fixture, album_fixture, song_fixture
):
    product = ProductFactory.create_product(
        product_cls_type_fixture, name_fixture, artist_fixture,
        price_fixture, product_type_fixture, album=album_fixture
    )
    assert all((
        song_fixture.name == product.name,
        song_fixture.artist == product.artist,
        song_fixture.price == product.price,
        song_fixture.product_type == product.product_type,
        song_fixture.album == product.album,
    ))
