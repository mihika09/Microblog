import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	print("\n\nos.environ.get('DATABASE_URL')", os.environ.get('DATABASE_URL'))
	print("DATABASE_URI: ", SQLALCHEMY_DATABASE_URI)
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['ginnyw0099@gmail.com']
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

	POSTS_PER_PAGE = 3
	LANGUAGES = ['en', 'es']
