from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post
from hashlib import md5


class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = User(username='Susan')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.check_password('cat'))

	def test_avatar(self):
		u = User(username='John', email='john@example.com')
		x = "hey8989" + u.email
		digest = md5(x.lower().encode('utf-8')).hexdigest()
		s = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, 128)
		self.assertTrue(u.avatar(128), s)

	def test_follow(self):
		u1 = User(username='John', email='john@example.com')
		u2 = User(username='Susan', email='susan@example.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u2.followed.all(), [])


