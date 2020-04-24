from flask_restplus import Namespace, fields


api_namespace = Namespace(
    'api', description='Albums microservice API operations'
)

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
    'price', type=float, required=True, help='Album price'
)
album_parser.add_argument(
    'genre', type=str, required=True, help='Album genre'
)
album_parser.add_argument(
    'description', type=str, required=True, help='Album description'
)

song_parser = auth_parser.copy()
song_parser.add_argument(
    'name', type=str, required=True, help='Song name'
)
song_parser.add_argument(
    'album_id', type=int, required=True, help='Album id'
)

search_parser = api_namespace.parser()
search_parser.add_argument(
    'search', type=str, required=False, help='Search in the albums'
)

album_model = api_namespace.model('Album', {
    'id': fields.Integer(),
    'name': fields.String(),
    'price': fields.Float(),
    'genre': fields.String(),
    'date': fields.DateTime(),
    'description': fields.String(),
    'artist_name': fields.String(),
    'artist_id': fields.Integer(),
})

song_model = api_namespace.model('Song', {
    'id': fields.Integer(),
    'name': fields.String(),
    'artist_name': fields.String(),
    'artist_id': fields.Integer(),
    'album_id': fields.Integer(),
})
