from flask import Flask
from flask_restplus import Api

from albums_backend.controllers import api_namespace
from albums_backend.database import db, db_config
from albums_backend.settings import app_config


def create_app():
    application = Flask(__name__)
    api = Api(
        application, version='0.0.1',
        title='Simple Music Explorer albums microservice API',
        description='Albums CRUD API'
    )
    application.config.update({**app_config, **db_config})
    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)

    return application
