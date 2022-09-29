from sqlalchemy.orm import backref
from movie import db, login_manager
from movie import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=40), nullable=False, unique=True)
    email_address=db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash=db.Column(db.String(length=60), nullable=False, unique=True)
    post_creator=db.relationship('Movies', backref='user')
    user_likes=db.relationship('Movies', secondary='likes')
    user_comments=db.relationship('Movies', secondary='comments')

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_password):
        self.password_hash=bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Likes(db.Model):
    __tablename__='likes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id=db.Column(db.Integer(), db.ForeignKey('user.id'))
    movies_id=db.Column(db.Integer(), db.ForeignKey('movies.id'))
    user=db.relationship('User', backref='likes')
    movies=db.relationship('Movies', backref='likes')


class Comments(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer(), primary_key=True)
    comment=db.Column(db.String(length=1000), nullable=False)
    user_id=db.Column(db.Integer(), db.ForeignKey('user.id'))
    movies_id=db.Column(db.Integer(), db.ForeignKey('movies.id'))
    user=db.relationship('User', backref='comments')
    movies=db.relationship('Movies', backref='comments')


class Movies(db.Model):
    __tablename__='movies'
    id=db.Column(db.Integer(), primary_key=True)
    movie_title=db.Column(db.String(length=50), nullable=False)
    poster_link=db.Column(db.String(length=600), unique=True)
    imdb_rating=db.Column(db.String(length=10), nullable=False)
    #rotten_tomatoe_rating=db.Column(db.String(length=5), nullable=False)
    story=db.Column(db.String(length=400), nullable=False)
    actors=db.Column(db.String(length=300), nullable=False)
    director=db.Column(db.String(length=100), nullable=False)
    awards=db.Column(db.String(length=200), nullable=False)
    genre=db.Column(db.String(length=100), nullable=False)
    post_creator=db.Column(db.Integer(), db.ForeignKey('user.username'))
    movie_likes=db.relationship('User', secondary='likes')
    movie_comments=db.relationship('User', secondary='comments')

'''
class UserInfo(db.Model):
    __tablename__='user_info'
    id= db.Column(db.Integer(), primary_key=True)
    first_name= db.Column(db.String(length=45))
    last_name= db.Column(db.String(length=45))
'''

db.create_all()
