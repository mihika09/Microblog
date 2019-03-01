from flask_mail import Message
from app import mail, app
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.text = text_body
	msg.html = html_body
	mail.send(msg)


def send_password_reset_email(user):
	token = user.get_password_reset_token()
	send_email('[Microblog] Password Reset', sender=app.config['ADMINS'][0], recipients=[user.email],
			text_body=render_template('email/reset_password.txt', user=user, token=token),
			html_body=render_template('email/reset_password.html', user=user, token=token))


# https://microblog-mihika.herokuapp.com/
# https://git.heroku.com/microblog-mihika.git
