import pytest
import http.client
from albums_backend.app import create_app
from .constants import PRIVATE_KEY
from albums_backend.token_validation import generate_token_header
from faker import Faker


fake = Faker()


@pytest.fixture
def app():
    app = create_app()

    app.app_context().push()
    # Initialise the DB
    app.db.create_all()

    return app


@pytest.fixture
def album_fixture(client):
    """
    Generate albums with songs in the system.
    """
    album_qty = 3
    songs_per_album = 2

    artist_name = fake.first_name()
    artist_id = fake.pyint()

    album_ids = []
    for i in range(album_qty):
        album = {
            'name': fake.text(15),
            'price': fake.pyint(),
            'genre': fake.text(10),
            'description': fake.text(128),
            'artist_name': artist_name,
            'artist_id': artist_id,
        }
        header = generate_token_header(artist_name, artist_id, PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post(
            '/api/artist/albums/', data=album, headers=headers
        )
        assert http.client.CREATED == response.status_code

        result = response.json
        album_ids.append({result['id']: []})

        for _ in range(songs_per_album):
            song = {
                'name': fake.text(15),
                'album_id': result['id'],
                'artist_name': artist_name,
                'artist_id': artist_id,
            }
            header = generate_token_header(artist_name, artist_id, PRIVATE_KEY)
            headers = {
                'Authorization': header,
            }
            response = client.post(
                f'/api/artist/albums/{result["id"]}/songs/', data=song, headers=headers
            )
            assert http.client.CREATED == response.status_code

            song_result = response.json
            album_ids[i][result['id']].append(song_result['id'])

    yield album_ids

    response = client.get('/api/albums/')
    albums = response.json
    for album in albums:
        album_id = album['id']
        header = generate_token_header(artist_name, artist_id, PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.delete(f'/api/artist/albums/{album_id}/', headers=headers)
        assert http.client.NO_CONTENT == response.status_code
