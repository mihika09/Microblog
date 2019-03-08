from app.main import bp
from flask import flash, redirect, render_template, url_for, request, g, current_app
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
from app import db
from flask_login import login_required, current_user
from datetime import datetime
from flask_babel import _, get_locale
from guess_language import guess_language


@bp.before_request
def before_request():
	g.locale = str(get_locale())
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	# user = User.query.filter_by(username=current_user.username).first_or_404()
	form = PostForm()
	page = request.args.get('page', 1, type=int)
	if form.validate_on_submit():
		print("Body: ", form.post.data, "Author: ", current_user, "and: ", current_user.username)
		language = guess_language(form.post.data)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''

		post = Post(body=form.post.data, author=current_user, language=language)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live!'))
		return redirect(url_for('main.index', page=page))

	posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title="Main Page", posts=posts.items, form=form, next_url=next_url, prev_url=prev_url, page=page)


@bp.route('/user/<username>')
@login_required
def user(username):

	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
	next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
	return render_template('user.html', title="title", user=user, posts=posts.items, prev_url=prev_url, next_url=next_url, page=page)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)

	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Successfully edited about me'))

		return redirect(url_for('main.edit_profile'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me

	return render_template('edit_profile.html', title="Edit Profile", form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash(_('User %(username)s not found', username=username))
		return redirect(url_for('main.index'))

	if current_user.username == username:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('main.user', username=username))

	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s', username=username))
	return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()

	if user is None:
		flash(_('User %(username)s not found',username=username))
		return redirect(url_for('main.index'))

	if current_user == user:
		flash(_('You cannot unfollow yourself'))
		return redirect(url_for('main.user', username=username))

	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are no longer following %(username)s',username=username))
	return redirect(url_for('main.user', username=username))


@bp.route('/following/<username>')
@login_required
def following(username):
	user = User.query.filter_by(username=username).first()
	return render_template('following.html', title='Following', user=user)


@bp.route('/followers/<username>')
@login_required
def followers(username):
	user = User.query.filter_by(username=username).first()
	return render_template('followers.html', title='Followers', user=user)


@bp.route('/explore')
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url, page=page)
