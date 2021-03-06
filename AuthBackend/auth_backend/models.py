from sqlalchemy import func

from auth_backend.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    date = db.Column(db.DateTime, server_default=func.now())
    is_active = db.Column(db.Boolean, default=False)

    artists = db.relationship(
        'ArtistModel', foreign_keys='ArtistModel.user_id',
        back_populates='user', cascade="all, delete-orphan"
    )


class ArtistModel(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=True)
    bio = db.Column(db.String(512), nullable=True)
    website = db.Column(db.String(32), nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )

    user = db.relationship('UserModel', back_populates='artists')
