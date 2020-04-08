import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

db_url = f'{BASE_DIR}/../catalog.db'

db_connection_url = f'sqlite+pysqlite:///{db_url}'

app_config = {
    'RESTPLUS_MASK_SWAGGER': False,
    'REQUEST_ID_UNIQUE_VALUE_PREFIX': '',
}

db_config = {
    'SQLALCHEMY_DATABASE_URI': db_connection_url.format(file_path=db_url),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'echo': False,
        'pool_recycle': 7200,
    },
}
