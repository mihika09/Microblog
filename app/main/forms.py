from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _


class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()], render_kw={"placeholder": _l("Username")})
	about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)], render_kw={"placeholder": _l("About Me")})
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		# print("original_username: ", original_username)
		# super().__init__(*args, **kwargs)
		# self.original_username = original_username
		# print("self.original_username: ", self.original_username)

		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			# print("Username: ", username, "username.data: ", username.data, "self.username.data: ", self.username.data)
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError(_('Please use  a different username'))


class PostForm(FlaskForm):
	post = TextAreaField(_l('Say Something!'), validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField(_l('Post!'))
