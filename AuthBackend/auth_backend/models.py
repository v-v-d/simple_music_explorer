from sqlalchemy import func

from auth_backend.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.Float, default=0)
    email = db.Column(db.String(32))
    date = db.Column(db.DateTime, server_default=func.now())


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
