from app import app, db
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    pic_file = db.Column(db.String(200), default = 'default.jpg')
    last_login = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    posts = db.relationship('Post', backref='author')

    def __repr__(self):
        return f'<User {self.email}>'

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(15), nullable = False)
    content = db.Column(db.String(50), nullable = False)
    posted_date = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f'<Post {self.title} by {self.author}'