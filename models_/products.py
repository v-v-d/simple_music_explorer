from models_.base import BaseProduct
from models_.exceptions import WrongInstanceError, WrongClassTypeError
from models_.mixins import PrototypeMixin


class Album(BaseProduct):
    def __init__(
            self, name, artist, price, product_type,
            album_format, genre, date, songs=None
    ):
        super().__init__(name, artist, price, product_type)
        self.album_format = album_format
        self.genre = genre
        self.date = date
        self.songs = songs or []

    def get_songs(self):
        return self.songs


class Song(BaseProduct, PrototypeMixin):
    def __init__(self, name, artist, price, product_type, album):
        super().__init__(name, artist, price, product_type)
        self.album = None
        self.set_album(album)

    def set_album(self, album):
        if isinstance(album, Album):
            self.album = album
        else:
            raise WrongInstanceError(
                f'Wrong album instance. Expected instance: {Album}.'
            )

    def get_artist(self):
        return self.artist

    def get_album(self):
        return self.album


class ProductFactory:
    types = {
        'Album': Album,
        'Song': Song,
    }

    @classmethod
    def create_product(cls, cls_type, name, artist, price, product_type, **kwargs):
        if cls_type not in cls.types:
            raise WrongClassTypeError(
                f'Wrong product type. Expected types: {", ".join(cls.types.keys())}'
            )
        product_cls = cls.types[cls_type]
        return product_cls(name, artist, price, product_type, **kwargs)
