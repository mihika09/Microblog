from datetime import datetime
from time import time
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from hashlib import md5
import jwt
from app import app

followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), db.Column(
	'followed_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), unique=True, index=True)
	email = db.Column(db.String(128), unique=True, index=True)
	password = db.Column(db.String(200), unique=True, index=True)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(
		followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	def __repr__(self):
		return "<User {}>".format(self.username)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def avatar(self, size):
		x = "hey8989"+self.email
		digest = md5(x.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def followed_posts(self):
		followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
			followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())

	def get_password_reset_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time()+expires_in}, app.config['SECRET_KEY'], algorithm='HS256'
		).decode('utf-8')

	@staticmethod
	def verify_password_reset_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']

		except:
			return
		return User.query.get(id)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class Post(db.Model):
	__searchable__ = ['body']
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	language = db.Column(db.String(5))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


