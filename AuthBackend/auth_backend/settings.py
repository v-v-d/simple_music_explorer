import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

app_config = {
    'RESTPLUS_MASK_SWAGGER': False,
    'REQUEST_ID_UNIQUE_VALUE_PREFIX': '',
}

mail_config = {
    'MAIL_SERVER': 'smtp.mail.ru',
    'MAIL_PORT': 465,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': 'simple_music_explorer@mail.ru',
    'MAIL_PASSWORD': 'Ra)1u1IiyiOE',
    'MAIL_DEFAULT_SENDER': 'simple_music_explorer@mail.ru',
}
