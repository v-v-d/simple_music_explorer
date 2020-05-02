from flask_restplus import Namespace, fields


admin_namespace = Namespace('admin', description='Admin operations')

api_namespace = Namespace(
    'api', description='Auth microservice API operations'
)

auth_parser = api_namespace.parser()
auth_parser.add_argument(
    'Authorization', location='headers', type=str,
    help='Bearer Access Token'
)

login_parser = api_namespace.parser()
login_parser.add_argument(
    'username', type=str, required=True, help='username'
)
login_parser.add_argument(
    'password', type=str, required=True, help='password'
)

register_parser = login_parser.copy()
register_parser.add_argument(
    'email', type=str, required=True, help='user email'
)


artist_parser = auth_parser.copy()
artist_parser.add_argument(
    'name', type=str, required=True, help='artist name'
)
artist_parser.add_argument(
    'location', type=str, required=False, help='artist location'
)
artist_parser.add_argument(
    'bio', type=str, required=False, help='artist bio'
)
artist_parser.add_argument(
    'label', type=str, required=False, help='artist record label'
)
artist_parser.add_argument(
    'website', type=str, required=False, help='artist website'
)

user_model = api_namespace.model('User', {
    'id': fields.Integer(),
    'name': fields.String(),
    'password': fields.String(),
    'email': fields.String(),
})

artist_model = api_namespace.model('Artist', {
    'id': fields.Integer(),
    'name': fields.String(),
    'location': fields.String(),
    'bio': fields.String(),
    'website': fields.Url(),
    'user_id': fields.Integer(),
})
