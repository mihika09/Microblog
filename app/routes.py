from app import app
from flask import flash, redirect, render_template, url_for
from app.forms import LoginForm


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():

	form = LoginForm()
	if form.validate_on_submit():
		flash("Hey, {}".format(form.username.data))
		return redirect(url_for('index'))

	return render_template('index.html', title="Login", form=form)
