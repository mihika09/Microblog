from app import app
from flask import flash, redirect, render_template, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm
from app.models import User, Post
from app import db
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	# user = User.query.filter_by(username=current_user.username).first_or_404()
	form = PostForm()
	page = request.args.get('page', 1, type=int)
	if form.validate_on_submit():
		print("Body: ", form.post.data, "Author: ", current_user, "and: ", current_user.username)
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index', page=page))

	posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title="Main Page", posts=posts.items, form=form, next_url=next_url, prev_url=prev_url, page=page)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		print("next_page: ", next_page)
		return redirect(next_page)

	return render_template('login.html', title="Login", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have successfully registered. Please login to continue')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username):

	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
	next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
	return render_template('user.html', title="title", user=user, posts=posts.items, prev_url=prev_url, next_url=next_url, page=page)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)

	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Successfully edited about me')

		return redirect(url_for('edit_profile'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me

	return render_template('edit_profile.html', title="Edit Profile", form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash('User {} not found'.format(username))
		return redirect(url_for('index'))

	if current_user.username == username:
		flash('You cannot follow yourself!')
		return redirect(url_for('user', username=username))

	current_user.follow(user)
	db.session.commit()
	flash('You are following {}'.format(username))
	return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()

	if user is None:
		flash('User {} not found'.format(username))
		return redirect(url_for('index'))

	if current_user == user:
		flash('You cannot unfollow yourself')
		return redirect(url_for('user', username=username))

	current_user.unfollow(user)
	db.session.commit()
	flash('You are no longer following {}'.format(username))
	return redirect(url_for('user', username=username))


@app.route('/following/<username>')
@login_required
def following(username):
	user = User.query.filter_by(username=username).first()
	return render_template('following.html', title='Following', user=user)


@app.route('/followers/<username>')
@login_required
def followers(username):
	user = User.query.filter_by(username=username).first()
	return render_template('followers.html', title='Followers', user=user)


@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url, page=page)


@app.route('/reset_password_request', methods=['GET', 'POST'])
@login_required
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = ResetPasswordRequestForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_reset_password_email(user)
			flash('Check your email for instructions to reset the password')
		else:
			flash('The email address hasn\'t been registered')

		return redirect(url_for('login'))

	return render_template('reset_password.html', title='Reset Password', form=form)



