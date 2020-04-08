from flask import Flask
from flask_restplus import Api

from catalog.controllers import api_namespace
from catalog.database import db
from catalog.settings import app_config, db_config


def create_app():
    app = Flask(__name__)
    api = Api(
        app, version='0.0.1', title='Simple Music Explorer catalog API',
        description='Catalog CRUD API'
    )
    app.config.update({**app_config, **db_config})
    db.init_app(app)
    app.db = db

    api.add_namespace(api_namespace)

    return app
