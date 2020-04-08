from datetime import datetime

from pytest import fixture

from models_.products import Album
from models_.users import Artist


@fixture()
def name_fixture():
    return 'Test name'


@fixture()
def artist_fixture():
    return Artist('test', 'test@test.com')


@fixture()
def price_fixture():
    return 100


@fixture()
def product_type_fixture():
    return 'Album'


@fixture()
def album_format_fixture():
    return 'LP'


@fixture()
def genre_fixture():
    return 'test'


@fixture()
def date_fixture():
    return datetime.now()


@fixture()
def album_fixture(
        name_fixture, artist_fixture, price_fixture, product_type_fixture,
        album_format_fixture, genre_fixture, date_fixture
):
    return Album(
        name_fixture, artist_fixture, price_fixture, product_type_fixture,
        album_format_fixture, genre_fixture, date_fixture
    )


def test_album_init(
        name_fixture, artist_fixture, price_fixture, product_type_fixture,
        album_format_fixture, genre_fixture, date_fixture, album_fixture
):
    assert all((
        album_fixture.name == name_fixture,
        album_fixture.artist == artist_fixture,
        album_fixture.price == price_fixture,
        album_fixture.product_type == product_type_fixture,
        album_fixture.album_format == album_format_fixture,
        album_fixture.genre == genre_fixture,
        album_fixture.date == date_fixture,
        not album_fixture.songs
    ))


def test_album_get_songs(album_fixture):
    assert type(album_fixture.get_songs()) == list
