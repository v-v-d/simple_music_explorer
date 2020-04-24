from sqlalchemy import func

from albums_backend.database import db


class AlbumModel(db.Model):
    __tablename__ = 'albums'
    __table_args__ = (
        db.CheckConstraint('price > 0'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, default=0)
    genre = db.Column(db.String(32))
    date = db.Column(db.DateTime, server_default=func.now())
    description = db.Column(db.String(512))
    artist_name = db.Column(db.String(128), nullable=False)
    artist_id = db.Column(db.Integer, nullable=False)

    songs = db.relationship(
        'SongModel', foreign_keys='SongModel.album_id',
        back_populates='album', cascade="all, delete-orphan"
    )
    # TODO: add a cover art


class SongModel(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    artist_name = db.Column(db.String(128), nullable=False)
    album_id = db.Column(
        db.Integer, db.ForeignKey('albums.id'), nullable=False
    )
    artist_id = db.Column(db.Integer, nullable=False)

    album = db.relationship('AlbumModel', back_populates='songs')
