import http.client
from datetime import datetime

from flask_restplus import Namespace, Resource, fields

from catalog.models import AlbumModel
from catalog.database import db
from catalog.utils import authentication_header_parser

api_namespace = Namespace('catalog', description='Catalog API operations')

auth_parser = api_namespace.parser()
auth_parser.add_argument(
    'Authorization', location='headers', type=str,
    help='Bearer Access Token'
)

album_parser = auth_parser.copy()
album_parser.add_argument(
    'name', type=str, required=True, help='Album name'
)
album_parser.add_argument(
    'price', type=int, required=True, help='Album price'
)
album_parser.add_argument(
    'genre', type=str, required=True, help='Album genre'
)
album_parser.add_argument(
    'description', type=str, required=True, help='Album description'
)

album_model = api_namespace.model('Album', {
    'id': fields.Integer(),
    'name': fields.String(),
    'price': fields.Float(),
    'genre': fields.String(),
    'date': fields.DateTime(),
    'description': fields.String(),
    'artist_id': fields.Integer(),
})

song_model = api_namespace.model('Song', {
    'id': fields.Integer(),
    'name': fields.String(),
    'price': fields.Float(),
    'artist_id': fields.Integer(),
    'album_id': fields.Integer(),
})


@api_namespace.route('/albums/')
class CreateAlbumController(Resource):
    @api_namespace.doc('create_album')
    @api_namespace.expect(album_parser)
    @api_namespace.marshal_with(album_model, code=http.client.CREATED)
    def post(self):
        args = album_parser.parse_args()
        artist = authentication_header_parser(args['Authorization'])

        artist_id = 0  # TODO: get artist id from other microservice db

        new_album = AlbumModel(
            name=args['name'],
            artist_id=artist_id,
            price=args['price'],
            genre=args['genre'],
            date=datetime.utcnow(),
            description=args['description']
        )

        db.session.add(new_album)
        db.session.commit()
        db.session.close()

        result = api_namespace.marshal(new_album, album_model)

        return result, http.client.CREATED


@api_namespace.route('/albums/')
class ReadAlbumsController(Resource):

    @api_namespace.doc('list_albums')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(album_model, as_list=True)
    def get(self):
        return AlbumModel.query.order_by('id').all()


@api_namespace.route('/albums/<int:album_id>/')
class AlbumController(Resource):

    @api_namespace.doc('list_albums')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(album_model, as_list=True)
    def get(self, album_id):
        return AlbumModel.query.query.get(album_id)

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass
