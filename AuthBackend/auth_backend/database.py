import os
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', 'SQLITE')

if DATABASE_ENGINE == 'SQLITE':
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path / '..'

    # Database initialisation
    FILE_PATH = f'{path}/db.sqlite3'
    DB_URI = f'sqlite+pysqlite:///{FILE_PATH}'
    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(file_path=FILE_PATH),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

elif DATABASE_ENGINE == 'POSTGRESQL':
    db_params = {
        'host': os.environ['POSTGRES_HOST'],
        'database': os.environ['POSTGRES_DB'],
        'user': os.environ['POSTGRES_USER'],
        'pwd': os.environ['POSTGRES_PASSWORD'],
        'port': os.environ['POSTGRES_PORT'],
    }
    DB_URI = f'postgresql://{db_params["user"]}:{db_params["pwd"]}' \
             f'@{db_params["host"]}:{db_params["port"]}/' \
             f'{db_params["database"]}'
    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(**db_params),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

else:
    raise Exception('Incorrect DATABASE_ENGINE')

db = SQLAlchemy()


# from contextlib import contextmanager
# Session = db.sessionmaker(bind=db.engine)
#
#
# @contextmanager
# def session_scope(expire_on_commit=True):
#     """Database connection context manager."""
#     if not isinstance(expire_on_commit, bool):
#         raise ValueError(
#             f'Expire attr must be bool. Got {type(expire_on_commit)}'
#         )
#
#     session = Session()
#     session.expire_on_commit = expire_on_commit
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()
