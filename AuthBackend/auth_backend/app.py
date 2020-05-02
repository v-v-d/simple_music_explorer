from flask import Flask
from flask_restplus import Api

from auth_backend.api_namespaces import admin_namespace
from auth_backend.controllers import api_namespace
from auth_backend.database import db, db_config
from auth_backend.settings import app_config


def create_app():
    application = Flask(__name__)
    api = Api(
        application, version='0.0.1',
        title='Simple Music Explorer auth microservice API',
        description='Auth CRUD API'
    )
    application.config.update({**app_config, **db_config})
    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)

    return application
