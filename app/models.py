from datetime import timedelta

from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from . import db


class ModelsMixins:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get(cls, tutorial_id, author_id):
        try:
            video = cls.query.filter(
                Video.id == tutorial_id,
                Video.author_id == author_id
            ).first()
            if not video:
                raise Exception('No tutorials with such an id')
        except Exception:
            db.session.rollback()
            raise
        return video

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


class Video(db.Model, ModelsMixins):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @classmethod
    def get_user_list(cls, author_id):
        try:
            videos = cls.query.filter(cls.author_id == author_id).all()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return videos

    @classmethod
    def get_list(cls):
        try:
            videos = cls.query.all()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return videos

    def __repr__(self) -> str:
        return self.name


class User(db.Model, ModelsMixins):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, index=True)
    email = db.Column(db.String(250), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    videos = db.relationship('Video', backref='author', lazy='dynamic')

    # Generate authorization token

    def generate_authorization_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    # Password

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hash(password)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password_hash):
            raise Exception('No user with such a password')
        return user

    def __repr__(self) -> str:
        return self.name
