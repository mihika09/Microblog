from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from flask_babel import _, lazy_gettext as _l


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


class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'), validators=[DataRequired(), Email()], render_kw={'autofocus': True})
	submit = SubmitField(_l('Submit'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()], render_kw={'autofocus': True})
	password2 = PasswordField(_l('Retype Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Request Password Reset'))
