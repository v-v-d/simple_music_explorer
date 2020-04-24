from faker import Faker

from albums_backend import token_validation
from .constants import PRIVATE_KEY

fake = Faker()


def get_user():
    return fake.first_name(), fake.pyint()


def get_headers(username, user_id):
    header = token_validation.generate_token_header(
        username, user_id, PRIVATE_KEY
    )

    return {
        'Authorization': header,
    }


def get_random_album(username, user_id):
    return {
        'name': fake.text(15),
        'price': abs(fake.pyfloat(3)),
        'genre': fake.text(10),
        'description': fake.text(128),
        'artist_name': username,
        'artist_id': user_id,
    }


def get_random_song(username, user_id, album_id):
    return {
        'name': fake.text(15),
        'album_id': album_id,
        'artist_name': username,
        'artist_id': user_id,
    }


def create_test_album(client, username, user_id, headers=None, **kwargs):
    new_album = get_random_album(username, user_id)

    if kwargs:
        [
            new_album.update({key: val})
            for key, val in kwargs.items()
            if key in new_album
        ]

    return (
        client.post(
            '/api/artist/albums/', data=new_album, headers=headers
        ),
        new_album
    )


def update_album(client, username, user_id, album_id, headers=None, **kwargs):
    upd_album = get_random_album(username, user_id)

    if kwargs:
        [
            upd_album.update({key: val})
            for key, val in kwargs.items()
            if key in upd_album
        ]

    return (
        client.patch(
            f'/api/artist/albums/{album_id}/', data=upd_album, headers=headers
        ),
        upd_album
    )


def create_test_song(
        client, username, user_id, album_id, headers=None, **kwargs
):
    new_song = get_random_song(username, user_id, album_id)

    if kwargs:
        [
            new_song.update({key: val})
            for key, val in kwargs.items()
            if key in new_song
        ]

    return (
        client.post(
            f'/api/artist/albums/{album_id}/songs/',
            data=new_song, headers=headers
        ),
        new_song
    )


def update_song(
        client, username, user_id, album_id, song_id, headers=None, **kwargs
):
    upd_song = get_random_song(username, user_id, album_id)

    if kwargs:
        [
            upd_song.update({key: val})
            for key, val in kwargs.items()
            if key in upd_song
        ]

    return (
        client.patch(
            f'/api/artist/songs/{song_id}/', data=upd_song, headers=headers
        ),
        upd_song
    )


def delete_test_album(client, album_id, headers=None):
    return client.delete(
        f'/api/artist/albums/{album_id}/', headers=headers
    )


def get_album_id_from_fixture(album_fixture):
    for key in album_fixture[0]:
        return key


def get_song_id_from_fixture(album_fixture):
    for key, val in album_fixture[0].items():
        return val[0]


def get_album_id_and_song_id_from_fixture(album_fixture):
    for key, val in album_fixture[0].items():
        return key, val[0]


def is_keys_valid(source, *expected_keys):
    return all((
        isinstance(source, dict),
        all(key in source for key in expected_keys)
    ))


def is_album_keys_valid(album):
    return is_keys_valid(
        album, 'id', 'name', 'price', 'genre', 'date',
        'description', 'artist_name', 'artist_id'
    )


def is_song_keys_valid(song):
    return is_keys_valid(
        song, 'id', 'name', 'album_id', 'artist_name', 'artist_id'
    )
