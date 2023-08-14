from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f"{self.text}"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def showtime(self):
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"{formatted_timestamp}"
    def __repr__(self):
        user = User.query.get(self.user_id)
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"by {user.username} ({formatted_timestamp})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post')
    def __repr__(self):
        user = User.query.get(self.user_id)
        return f"Made by {user.username}"
    def showtime(self):
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"{formatted_timestamp}"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.relationship('Note', backref='user') # One to many
    comments = db.relationship('Comment', backref='user')
    posts = db.relationship('Post', backref='user') 
    def showdate(self):
        formatted_date = self.date_joined.strftime("%d %B %Y")
        return f"{formatted_date}"
    def __repr__(self):
        return f"<{self.username}>"