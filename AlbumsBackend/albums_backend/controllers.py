import http.client
from datetime import datetime

from flask_restplus import Resource

from albums_backend.api_namespaces import (
    api_namespace, auth_parser, album_parser, search_parser,
    album_model, song_model,song_parser, admin_namespace
)
from albums_backend.models import AlbumModel, SongModel
from albums_backend.database import db
from albums_backend.utils import authentication_header_parser


@api_namespace.route('/artist/albums/')
class ArtistAlbumsController(Resource):

    @api_namespace.doc('list_artist_albums')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(album_model, as_list=True)
    def get(self):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_albums = (
            AlbumModel.query
            .filter_by(artist_id=artist['id'])
            .order_by('id')
            .all()
        )
        return artist_albums

    @api_namespace.doc('create_album')
    @api_namespace.expect(album_parser)
    @api_namespace.marshal_with(album_model, code=http.client.CREATED)
    def post(self):
        args = album_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        if args['price'] < 0:
            return '', http.client.BAD_REQUEST

        new_album = AlbumModel(
            name=args['name'],
            price=args['price'],
            genre=args['genre'],
            date=datetime.utcnow(),
            description=args['description'],
            artist_name=artist['name'],
            artist_id=artist['id']
        )

        db.session.add(new_album)
        db.session.commit()

        result = api_namespace.marshal(new_album, album_model)

        return result, http.client.CREATED


@api_namespace.route('/artist/albums/<int:album_id>/')
class ArtistAlbumController(Resource):

    @api_namespace.doc('retrieve_artist_album')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(album_model)
    def get(self, album_id):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_album = (
            AlbumModel.query
            .filter_by(id=album_id, artist_id=artist['id'])
            .first()
        )

        if not artist_album:
            return '', http.client.NOT_FOUND

        return artist_album

    @api_namespace.doc('update_album')
    @api_namespace.expect(album_parser)
    @api_namespace.marshal_with(album_model, code=http.client.OK)
    def patch(self, album_id):
        args = album_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_album = (
            AlbumModel.query
            .filter_by(id=album_id, artist_id=artist['id'])
            .first()
        )

        if not artist_album:
            return '', http.client.NOT_FOUND

        for key, val in args.items():
            if hasattr(artist_album, key):
                setattr(artist_album, key, val)

        db.session.commit()

        result = api_namespace.marshal(artist_album, album_model)

        return result, http.client.OK

    @api_namespace.doc(
        'delete_album', responses={http.client.NO_CONTENT: 'No content'}
    )
    @api_namespace.expect(auth_parser)
    def delete(self, album_id):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_album = (
            AlbumModel.query
            .filter_by(id=album_id, artist_id=artist['id'])
            .first()
        )

        if not artist_album:
            return '', http.client.NOT_FOUND

        db.session.delete(artist_album)
        db.session.commit()

        return '', http.client.NO_CONTENT


@api_namespace.route('/artist/albums/<int:album_id>/songs/')
class ArtistAlbumSongsController(Resource):

    @api_namespace.doc('list_artist_album_songs')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(song_model, as_list=True)
    def get(self, album_id):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_album_songs = (
            SongModel.query
            .filter_by(artist_id=artist['id'], album_id=album_id)
            .order_by('id')
            .all()
        )

        return artist_album_songs

    @api_namespace.doc('create_album_song')
    @api_namespace.expect(song_parser)
    @api_namespace.marshal_with(song_model, code=http.client.CREATED)
    def post(self, album_id):
        args = song_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_album = (
            AlbumModel.query
            .filter_by(artist_id=artist['id'], id=album_id)
            .first()
        )

        if not artist_album:
            return '', http.client.NOT_FOUND

        new_song = SongModel(
            name=args['name'],
            artist_name=artist['name'],
            artist_id=artist['id'],
            album_id=album_id
        )

        db.session.add(new_song)
        db.session.commit()

        result = api_namespace.marshal(new_song, song_model)

        return result, http.client.CREATED


@api_namespace.route('/artist/songs/<int:song_id>/')
class ArtistAlbumSongController(Resource):

    @api_namespace.doc('retrieve_artist_song')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(song_model)
    def get(self, song_id):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_song = (
            SongModel.query
            .filter_by(id=song_id, artist_id=artist['id'])
            .first()
        )

        if not artist_song:
            return '', http.client.NOT_FOUND

        return artist_song

    @api_namespace.doc('update_song')
    @api_namespace.expect(song_parser)
    @api_namespace.marshal_with(song_model, code=http.client.OK)
    def patch(self, song_id):
        args = song_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_song = (
            SongModel.query
            .filter_by(id=song_id, artist_id=artist['id'])
            .first()
        )

        if not artist_song:
            return '', http.client.NOT_FOUND

        for key, val in args.items():
            if hasattr(artist_song, key):
                setattr(artist_song, key, val)

        db.session.commit()

        result = api_namespace.marshal(artist_song, song_model)

        return result, http.client.OK

    @api_namespace.doc(
        'delete_song', responses={http.client.NO_CONTENT: 'No content'}
    )
    @api_namespace.expect(auth_parser)
    def delete(self, song_id):
        args = auth_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_song = (
            SongModel.query
            .filter_by(id=song_id, artist_id=artist['id'])
            .first()
        )

        if artist_song:
            db.session.delete(artist_song)
            db.session.commit()

        return '', http.client.NO_CONTENT


@api_namespace.route('/albums/')
class AllAlbumsController(Resource):

    @api_namespace.doc('list_all_albums')
    @api_namespace.expect(search_parser)
    @api_namespace.marshal_with(album_model, as_list=True)
    def get(self):
        args = search_parser.parse_args()
        search_param = args['search']
        query = AlbumModel.query

        if search_param:
            param = f'%{search_param}%'
            query = (query.filter(AlbumModel.name.ilike(param)))

        albums = query.order_by('id').all()

        return albums


@api_namespace.route('/albums/<int:album_id>/')
class AlbumController(Resource):

    @api_namespace.doc('retrieve_album')
    @api_namespace.marshal_with(album_model)
    def get(self, album_id):
        album = AlbumModel.query.get(album_id)

        if not album:
            return '', http.client.NOT_FOUND

        return album


@api_namespace.route('/albums/<int:album_id>/songs/')
class SongsController(Resource):

    @api_namespace.doc('retrieve_songs')
    @api_namespace.marshal_with(song_model, as_list=True)
    def get(self, album_id):
        songs = (
            SongModel.query
            .filter_by(album_id=album_id)
            .order_by('id')
            .all()
        )

        if not songs:
            return '', http.client.NOT_FOUND

        return songs


@api_namespace.route('/songs/<int:song_id>/')
class SongController(Resource):

    @api_namespace.doc('retrieve_song')
    @api_namespace.marshal_with(song_model, as_list=True)
    def get(self, song_id):
        song = SongModel.query.get(song_id)

        if not song:
            return '', http.client.NOT_FOUND

        return song


@admin_namespace.route('/albums/<int:album_id>/')
class DeleteAlbumController(Resource):

    @admin_namespace.doc(
        'delete_album', responses={http.client.NO_CONTENT: 'No content'}
    )
    def delete(self, album_id):
        album = AlbumModel.query.get(album_id)

        if album:
            db.session.delete(album)
            db.session.commit()

        return '', http.client.NO_CONTENT
