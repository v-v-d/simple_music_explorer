"""
Test the Albums operations


Use the album_fixture to have data to retrieve, it generates three albums
"""
import http.client
from unittest.mock import ANY

from freezegun import freeze_time

from .utils import (
    is_album_keys_valid, is_song_keys_valid, get_user, get_headers,
    create_test_album, delete_test_album, get_album_id_from_fixture,
    get_song_id_from_fixture, get_album_id_and_song_id_from_fixture,
    update_album, create_test_song, update_song
)


# @freeze_time('2019-05-07 13:47:34')
# def test_create_album(client):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response, new_album = create_test_album(client, username, user_id, headers)
#     result = response.json
#
#     assert http.client.CREATED == response.status_code
#
#     expected = {
#         'id': ANY,
#         'name': new_album['name'],
#         'price': new_album['price'],
#         'genre': new_album['genre'],
#         'date': '2019-05-07T13:47:34',
#         'description': new_album['description'],
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#     assert result == expected
#
#     response = delete_test_album(client, result['id'], headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_create_album_unauthorized(client):
#     username, user_id = get_user()
#     response, new_album = create_test_album(client, username, user_id)
#
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_list_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     response_get_albums = client.get('/api/artist/albums/', headers=headers)
#     albums = response_get_albums.json
#
#     assert http.client.OK == response_get_albums.status_code
#     assert len(albums) == 1
#
#     album = albums[0]
#     expected = {
#         'id': ANY,
#         'name': new_album['name'],
#         'price': new_album['price'],
#         'genre': new_album['genre'],
#         'date': ANY,
#         'description': new_album['description'],
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#
#     assert album == expected
#
#     response = delete_test_album(
#         client, response_new_album.json['id'], headers
#     )
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_get_list_artist_album_unauthorized(client):
#     response = client.get('/api/artist/albums/')
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_list_all_albums(client, album_fixture):
#     response = client.get('/api/albums/')
#     albums = response.json
#
#     assert http.client.OK == response.status_code
#     assert len(albums) > 0
#
#     # Check that the ids are increasing
#     previous_id = -1
#     for album in albums:
#         assert is_album_keys_valid(album)
#         assert album['id'] > previous_id
#         previous_id = album['id']
#
#
# def test_get_list_all_albums_search(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers, name='This is a TestAlbumName'
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     response = client.get('/api/albums/?search=testalbumname')
#     albums = response.json
#
#     assert http.client.OK == response.status_code
#     assert len(albums) > 0
#
#     for album in albums:
#         assert is_album_keys_valid(album)
#         assert 'testalbumname' in album['name'].lower()
#
#     response = delete_test_album(
#         client, response_new_album.json['id'], headers
#     )
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_get_album(client, album_fixture):
#     album_id = get_album_id_from_fixture(album_fixture)
#     response = client.get(f'/api/albums/{album_id}/')
#     result = response.json
#
#     assert http.client.OK == response.status_code
#     assert is_album_keys_valid(result)
#
#
# def test_get_non_existing_album(client, album_fixture):
#     album_id = 123456
#     response = client.get(f'/api/albums/{album_id}/')
#
#     assert http.client.NOT_FOUND == response.status_code
#
#
# def test_get_list_album_songs(client, album_fixture):
#     album_id = get_album_id_from_fixture(album_fixture)
#     response = client.get(f'/api/albums/{album_id}/songs/')
#     songs = response.json
#
#     assert http.client.OK == response.status_code
#     assert len(songs) > 0
#
#     # Check that the ids are increasing
#     previous_id = -1
#     for song in songs:
#         expected = {
#             'id': ANY,
#             'name': ANY,
#             'album_id': album_id,
#             'artist_name': ANY,
#             'artist_id': ANY,
#         }
#         assert expected == song
#         assert song['id'] > previous_id
#         previous_id = song['id']
#
#
# def test_get_list_songs_of_non_existing_album(client, album_fixture):
#     album_id = 123456
#     response = client.get(f'/api/albums/{album_id}/songs/')
#
#     assert http.client.NOT_FOUND == response.status_code
#
#
# def test_get_song(client, album_fixture):
#     song_id = get_song_id_from_fixture(album_fixture)
#     response = client.get(f'/api/songs/{song_id}/')
#     song = response.json
#
#     assert http.client.OK == response.status_code
#     assert is_song_keys_valid(song)
#
#
# def test_get_non_existing_song(client, album_fixture):
#     song_id = 123456
#     response = client.get(f'/api/songs/{song_id}/')
#
#     assert http.client.NOT_FOUND == response.status_code
#
#
# def test_get_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#     album_id = response_new_album.json['id']
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     response = client.get(f'/api/artist/albums/{album_id}/', headers=headers)
#     album = response.json
#
#     assert http.client.OK == response.status_code
#     assert is_album_keys_valid(album)
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_get_artist_album_unauthorized(client, album_fixture):
#     album_id = get_album_id_from_fixture(album_fixture)
#     response = client.get(f'/api/artist/albums/{album_id}/')
#
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_non_existing_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     album_id = 123456
#     response = client.get(f'/api/artist/albums/{album_id}/', headers=headers)
#
#     assert http.client.NOT_FOUND == response.status_code
#
#
# @freeze_time('2019-05-07 13:47:34')
# def test_update_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_upd_album, upd_album = update_album(
#         client, username, user_id, album_id, headers
#     )
#     result = response_upd_album.json
#
#     assert http.client.OK == response_upd_album.status_code
#
#     expected = {
#         'id': ANY,
#         'name': upd_album['name'],
#         'price': upd_album['price'],
#         'genre': upd_album['genre'],
#         'date': '2019-05-07T13:47:34',
#         'description': upd_album['description'],
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#     assert result == expected
#
#     response = delete_test_album(
#         client, response_new_album.json['id'], headers
#     )
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_update_artist_album_unauthorized(client, album_fixture):
#     username, user_id = get_user()
#     album_id = get_album_id_from_fixture(album_fixture)
#     response_upd_album, upd_album = update_album(
#         client, username, user_id, album_id
#     )
#
#     assert http.client.UNAUTHORIZED == response_upd_album.status_code
#
#
# def test_update_non_existing_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     album_id = 123456
#     response_upd_album, upd_album = update_album(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.NOT_FOUND == response_upd_album.status_code
#
#
# def test_delete_artist_album_unauthorized(client, album_fixture):
#     album_id = get_album_id_from_fixture(album_fixture)
#     response = client.delete(f'/api/artist/albums/{album_id}/')
#
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_list_artist_album_songs(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     response = client.get(
#         f'/api/artist/albums/{album_id}/songs/', headers=headers
#     )
#     songs = response.json
#
#     assert http.client.OK == response.status_code
#     assert len(songs) == 1
#
#     result = songs[0]
#     expected_result = {
#         'id': ANY,
#         'name': new_song['name'],
#         'album_id': album_id,
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#     assert result == expected_result
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_get_list_artist_album_songs_unauthorized(client, album_fixture):
#     album_id = get_album_id_from_fixture(album_fixture)
#     response = client.get(f'/api/artist/albums/{album_id}/songs/')
#
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_list_songs_of_non_existing_artist_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     album_id = 123456
#     response = client.get(
#         f'/api/artist/albums/{album_id}/songs/', headers=headers
#     )
#     result = response.json
#
#     assert isinstance(result, list) and not result
#
#
# def test_create_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#     song = response_new_song.json
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     expected = {
#         'id': ANY,
#         'name': new_song['name'],
#         'album_id': album_id,
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#     assert song == expected
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_create_song_unauthorized(client, album_fixture):
#     username, user_id = get_user()
#     album_id = get_album_id_from_fixture(album_fixture)
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id
#     )
#
#     assert http.client.UNAUTHORIZED == response_new_song.status_code
#
#
# def test_create_song_of_non_existing_album(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     album_id = 123456
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.NOT_FOUND == response_new_song.status_code
#
#
# def test_get_artist_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     song_id = response_new_song.json['id']
#     response = client.get(f'/api/artist/songs/{song_id}/', headers=headers)
#     result = response.json
#
#     assert http.client.OK == response.status_code
#     assert is_song_keys_valid(result)
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_get_artist_song_unauthorized(client, album_fixture):
#     song_id = get_song_id_from_fixture(album_fixture)
#     response = client.get(f'/api/artist/songs/{song_id}/')
#
#     assert http.client.UNAUTHORIZED == response.status_code
#
#
# def test_get_non_existing_artist_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     song_id = 123456
#     response = client.get(f'/api/artist/songs/{song_id}/', headers=headers)
#
#     assert http.client.NOT_FOUND == response.status_code
#
#
# def test_update_artist_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     song_id = response_new_song.json['id']
#     response_upd_song, upd_song = update_song(
#         client, username, user_id, album_id, song_id, headers
#     )
#     result = response_upd_song.json
#
#     assert http.client.OK == response_upd_song.status_code
#
#     expected = {
#         'id': song_id,
#         'name': upd_song['name'],
#         'album_id': album_id,
#         'artist_name': username,
#         'artist_id': user_id,
#     }
#     assert result == expected
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_update_artist_song_unauthorized(client, album_fixture):
#     username, user_id = get_user()
#     album_id, song_id = get_album_id_and_song_id_from_fixture(album_fixture)
#     response_upd_song, upd_song = update_song(
#         client, username, user_id, album_id, song_id
#     )
#
#     assert http.client.UNAUTHORIZED == response_upd_song.status_code
#
#
# def test_update_non_existing_artist_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     song_id = 123456
#     response_upd_song, upd_song = update_song(
#         client, username, user_id, album_id, song_id, headers
#     )
#
#     assert http.client.NOT_FOUND == response_upd_song.status_code
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_delete_artist_song(client, album_fixture):
#     username, user_id = get_user()
#     headers = get_headers(username, user_id)
#     response_new_album, new_album = create_test_album(
#         client, username, user_id, headers
#     )
#
#     assert http.client.CREATED == response_new_album.status_code
#
#     album_id = response_new_album.json['id']
#     response_new_song, new_song = create_test_song(
#         client, username, user_id, album_id, headers
#     )
#
#     assert http.client.CREATED == response_new_song.status_code
#
#     song_id = response_new_song.json['id']
#     response = client.delete(f'/api/artist/songs/{song_id}/', headers=headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#     response = delete_test_album(client, album_id, headers)
#     assert http.client.NO_CONTENT == response.status_code
#
#
# def test_delete_artist_song_unauthorized(client, album_fixture):
#     song_id = get_song_id_from_fixture(album_fixture)
#     response = client.delete(f'/api/artist/songs/{song_id}/')
#
#     assert http.client.UNAUTHORIZED == response.status_code


def test_delete_album_by_admin(client):
    username, user_id = get_user()
    headers = get_headers(username, user_id)
    response, new_album = create_test_album(client, username, user_id, headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'name': new_album['name'],
        'price': new_album['price'],
        'genre': new_album['genre'],
        'date': ANY,
        'description': new_album['description'],
        'artist_name': username,
        'artist_id': user_id,
    }
    assert result == expected

    response = client.delete(f'/admin/albums/{result["id"]}/')
    assert http.client.NO_CONTENT == response.status_code
