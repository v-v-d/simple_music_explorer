import http.client
from datetime import datetime

from flask import request
from flask_restplus import Resource

from auth_backend import config
from auth_backend.api_namespaces import (
    admin_namespace, api_namespace, auth_parser, login_parser,
    register_parser, user_model, delete_parser, artist_parser,
    artist_model
)
from auth_backend.database import db
from auth_backend.email_token_generator import check_token
from auth_backend.models import UserModel, ArtistModel
from auth_backend.token_validation import generate_token_header
from auth_backend.utils import (
    authentication_header_parser, get_password_digest, send_verify_email,
    urlsafe_base64_decode, is_password_valid
)


@api_namespace.route('/auth/register/')
class RegisterController(Resource):

    @api_namespace.expect(register_parser)
    def post(self):
        """
        Register and send a verifying email
        """
        args = register_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if password != args['password2']:
            return '', http.client.BAD_REQUEST

        password_digest = get_password_digest(password)

        new_user = UserModel(
            name=username, password=password_digest,
            email=email, date=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()

        url_root = request.url_root
        domain = request.headers['Host']

        if send_verify_email(email, url_root, domain, username, False):
            return '', http.client.OK
        else:
            user = UserModel.query.filter_by(name=username).first()
            db.session.delete(user)
            db.session.commit()

            return 'email sending error', http.client.BAD_REQUEST


@api_namespace.route('/auth/activate/<string:unameb64>/<string:token>/')
class UserActivateController(Resource):

    def post(self, unameb64, token):
        """
        Activate user account by link from verifying email
        """
        try:
            username = urlsafe_base64_decode(unameb64).decode()

        except ValueError as error:
            print('ValueError:', error)

        else:
            if token:
                if check_token(username, False, token):
                    user = UserModel.query.filter_by(name=username).first()

                    if user:
                        user.is_active = True
                        db.session.commit()

                        header = generate_token_header(
                            user.name, user.id, config.PRIVATE_KEY
                        )

                        return {'Authorized': header}, http.client.OK

        return 'Activation link is invalid!', http.client.BAD_REQUEST


@api_namespace.route('/auth/login/')
class LoginController(Resource):

    @api_namespace.doc('login')
    @api_namespace.expect(login_parser)
    def post(self):
        """
        Login and return a valid Authorization header
        """
        args = login_parser.parse_args()

        user = UserModel.query.filter_by(name=args['username']).first()

        if user and user.is_active and is_password_valid(
                user, args['password']
        ):
            header = generate_token_header(
                user.name, user.id, config.PRIVATE_KEY
            )
            return {'Authorized': header}, http.client.OK

        return '', http.client.UNAUTHORIZED


@api_namespace.route('/auth/logout/')
class LogoutController(Resource):

    @api_namespace.doc('logout')
    @api_namespace.expect(auth_parser)
    def post(self):
        args = auth_parser.parse_args()
        user = authentication_header_parser(args['Authorization'])

        if user:
            return {'Authorized': None}, http.client.OK

        return '', http.client.UNAUTHORIZED


@api_namespace.route('/auth/')
class AuthController(Resource):

    @api_namespace.doc('get_user')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(user_model)
    def get(self):
        args = auth_parser.parse_args()
        user_data = authentication_header_parser(args['Authorization'])

        user = UserModel.query.filter_by(id=user_data['id']).first()

        if not user:
            return '', http.client.NOT_FOUND

        return user

    @api_namespace.doc('delete_user')
    @api_namespace.expect(delete_parser)
    def delete(self):
        args = delete_parser.parse_args()
        user_data = authentication_header_parser(args['Authorization'])

        user = UserModel.query.filter_by(id=user_data['id']).first()

        if user:
            if not is_password_valid(user, args['password']):
                return '', http.client.BAD_REQUEST

            db.session.delete(user)
            db.session.commit()

        return '', http.client.NO_CONTENT


@api_namespace.route('/artist/')
class ArtistController(Resource):

    @api_namespace.doc('get_artist')
    @api_namespace.expect(auth_parser)
    @api_namespace.marshal_with(artist_model)
    def get(self):
        args = auth_parser.parse_args()
        user = authentication_header_parser(args['Authorization'])

        artist = ArtistModel.query.filter_by(user_id=user['id']).first()

        if not artist:
            return '', http.client.NOT_FOUND

        return artist

    @api_namespace.doc('create_artist')
    @api_namespace.expect(artist_parser)
    @api_namespace.marshal_with(artist_model, code=http.client.CREATED)
    def post(self):
        args = artist_parser.parse_args()
        user = authentication_header_parser(args['Authorization'])

        new_artist = ArtistModel(
            name=args['name'],
            location=args['location'],
            bio=args['bio'],
            website=args['website'],
            user_id=user['id']
        )

        db.session.add(new_artist)
        db.session.commit()

        result = api_namespace.marshal(new_artist, artist_model)

        return result, http.client.CREATED

    @api_namespace.doc('update_artist')
    @api_namespace.expect(artist_parser)
    @api_namespace.marshal_with(artist_model, code=http.client.OK)
    def patch(self):
        args = artist_parser.parse_args()
        user = authentication_header_parser(args['Authorization'])

        artist = ArtistModel.query.filter_by(user_id=user['id']).first()

        if not artist:
            return '', http.client.NOT_FOUND

        for key, val in args.items():
            if hasattr(artist, key):
                setattr(artist, key, val)

        db.session.commit()

        result = api_namespace.marshal(artist, artist_model)

        return result, http.client.OK

    @api_namespace.doc('delete_artist')
    @api_namespace.expect(delete_parser)
    def delete(self):
        args = delete_parser.parse_args()
        user = authentication_header_parser(args['Authorization'])

        artist = ArtistModel.query.filter_by(user_id=user['id']).first()

        if artist:
            if not is_password_valid(artist.user, args['password']):
                return '', http.client.BAD_REQUEST

            db.session.delete(artist)
            db.session.commit()

        return '', http.client.NO_CONTENT


@admin_namespace.route('/auth/<int:user_id>/')
class AdminDeleteUserController(Resource):

    @admin_namespace.doc(
        'delete_user', responses={http.client.NO_CONTENT: 'No content'}
    )
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

        return '', http.client.NO_CONTENT


@admin_namespace.route('/artist/<int:artist_id>/')
class AdminDeleteArtistController(Resource):

    @admin_namespace.doc(
        'delete_artist', responses={http.client.NO_CONTENT: 'No content'}
    )
    def delete(self, artist_id):
        artist = ArtistModel.query.filter_by(id=artist_id).first()

        if artist:
            db.session.delete(artist)
            db.session.commit()

        return '', http.client.NO_CONTENT
