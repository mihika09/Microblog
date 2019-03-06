from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _


class LoginForm(FlaskForm):

	username = StringField(_l("Username"), validators=[DataRequired()], render_kw={"placeholder": _l("Username"), "autofocus": True})
	password = PasswordField(_l("Password"), validators=[DataRequired()], render_kw={"placeholder": _l("Password")})
	remember_me = BooleanField(_l("Remember Me"))
	submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):

	username = StringField(_l("Username"), validators=[DataRequired()], render_kw={"placeholder": _l("Username"), "autofocus": True})
	email = StringField(_l("Email"), validators=[DataRequired(), Email()], render_kw={"placeholder": _l("Email")})
	password = PasswordField(_l("Password"), validators=[DataRequired()], render_kw={"placeholder": _l("Password")})
	password2 = PasswordField(_l("Retype Password"), validators=[DataRequired(), EqualTo('password')], render_kw={
		"placeholder": _l("Retype Password")})
	submit = SubmitField(_l("Register"))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_('Username already exists. Please enter another username'))

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError(_('Email already registered. Please try and login'))


class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": _l("Username")})
	about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)], render_kw={"placeholder": _l("About Me")})
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		print("original_username: ", original_username)
		super().__init__(*args, **kwargs)
		self.original_username = original_username
		print("self.original_username: ", self.original_username)

	def validate_username(self, username):
		if username.data != self.original_username:
			print("Username: ", username, "username.data: ", username.data, "self.username.data: ", self.username.data)
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError(_('Please use  a different username'))


class PostForm(FlaskForm):
	post = TextAreaField(_l('Say Something!'), validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField(_l('Post!'))


class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={'autofocus': True})
	submit = SubmitField(_l('Submit'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()], render_kw={'autofocus': True})
	password2 = PasswordField(_l('Retype Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Request Password Reset'))
