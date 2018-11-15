from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from thermos import db

tags = db.Table('bookmark_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
                )

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return f"<Bookmark '{self.description}': '{self.url}'>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f"<User {self.username}>"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.name
