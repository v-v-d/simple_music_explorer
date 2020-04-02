from models.base import BaseUser


class Artist(BaseUser):
    def __init__(self, name, email, albums=None, songs=None):
        super().__init__(name, email)
        self.albums = albums or []
        self.songs = songs or []

    def get_albums(self):
        return self.albums

    def get_songs(self):
        return self.songs

    def add_album(self, album):
        self.albums.append(album)

    def add_song(self, song):
        self.songs.append(song)


class User(BaseUser):
    def __init__(self, name, email, last_name):
        super().__init__(name, email)
        self.last_name = last_name

    def get_full_name(self):
        return f'{self.name} {self.last_name}'


class UserFactory:
    types = {
        'Artist': Artist,
        'User': User,
    }

    @classmethod
    def create_user(cls, cls_type, name, email, **kwargs):
        user_cls = cls.types[cls_type]
        return user_cls(name, email, **kwargs)
