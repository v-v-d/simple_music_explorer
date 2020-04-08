from sqlalchemy import func

from catalog.database import db


class AlbumModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Float)
    genre = db.Column(db.String(32))
    date = db.Column(db.DateTime, server_default=func.now())
    description = db.Column(db.String(512))
    artist_id = db.Column(db.Integer)
    # TODO: add a cover art


class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Float)
    artist_id = db.Column(db.Integer)
    album_id = db.Column(db.Integer)
