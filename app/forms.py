from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username", "autofocus": True})
	password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Log In")
