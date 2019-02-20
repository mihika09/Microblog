from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):

	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username", "autofocus": True})
	password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember_me = BooleanField("Remember Me")
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username", "autofocus": True})
	email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
	password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
	password2 = PasswordField("Retype Password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Retype Password"})
	submit = SubmitField("Register")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already exists. Please enter another username')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError('Email already registered. Please try and login')
