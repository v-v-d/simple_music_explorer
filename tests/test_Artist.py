from pytest import fixture

from models.users import Artist


@fixture()
def artist_name_fixture():
    return 'Homer'


@fixture()
def email_fixture():
    return 'homer@mail.com'


@fixture()
def artist_fixture(artist_name_fixture, email_fixture):
    return Artist(artist_name_fixture, email_fixture)


def test_artist_init(artist_fixture, artist_name_fixture, email_fixture):
    assert all((
        artist_fixture.name == artist_name_fixture,
        artist_fixture.email == email_fixture,
        type(artist_fixture.albums) == list,
        type(artist_fixture.songs) == list,
    ))


def test_artist_get_albums(artist_fixture):
    assert type(artist_fixture.get_albums()) == list


def test_artist_get_songs(artist_fixture):
    assert type(artist_fixture.get_songs()) == list
