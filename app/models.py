from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    favorites = db.relationship('Favorite', backref='author', lazy='dynamic')
    youtube_channel_id = db.Column(db.String(255), unique=True)
    youtube_channel_name = db.Column(db.String(255))
    youtube_channel_description = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idea = db.Column(db.Text, nullable=False)
    script = db.Column(db.Text)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    hashtags = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite {self.idea[:30]}>'

db.create_all()