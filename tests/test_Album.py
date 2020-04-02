from datetime import datetime

from pytest import fixture, raises

from models.exceptions import WrongInstanceError
from models.products import Song, Album
from models.users import Artist


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


def test_song_init(
        name_fixture, artist_fixture, price_fixture,
        product_type_fixture, album_fixture, song_fixture
):
    assert all((
        song_fixture.name == name_fixture,
        song_fixture.artist == artist_fixture,
        song_fixture.price == price_fixture,
        song_fixture.product_type == product_type_fixture,
        song_fixture.album == album_fixture
    ))


def test_song_set_album(song_fixture, album_fixture):
    song_fixture.set_album(album_fixture)
    assert song_fixture.album == album_fixture


def test_song_set_album_invalid(song_fixture):
    with raises(WrongInstanceError):
        assert song_fixture.set_album('invalid album instance')


def test_song_get_artist(song_fixture, artist_fixture):
    assert song_fixture.get_artist() == artist_fixture


def test_song_get_album(song_fixture, album_fixture):
    assert song_fixture.get_album() == album_fixture
