import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, redirect, request, abort
from flaskapp import app, db, bcrypt, mail
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskapp.models import User, Post, Affiliation, PostRecipient
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_paginate import Pagination, get_page_args


# Specifies the web directory, in this case, the root/homepage
@app.route('/')
@app.route('/home')  # multiple decorators handled by the same function
@login_required
def home():
    if current_user.provider:
        return redirect(url_for("affiliation_posts", id=current_user.affiliation.id))
    elif current_user.distributor:
        return redirect(url_for("unread_posts"))


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])  # allowed HTML methods
def register():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add form received data to db model
        if form.type.data == "Provider":
            provider = 1
            distributor = 0
        else:  # form.type.data == "Distributor"
            provider = 0
            distributor = 1
        hashed_password = \
            bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash password and decode hash to string
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin = 0,
                    affiliation=form.affiliation.data, provider=provider, distributor=distributor)

        # Add created model to db and commit
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully.", 'success')  # success: bootstrap class
        return redirect(url_for('account'))
    return render_template('register.html', title="Registration Form", form=form)


@app.route('/login', methods=['GET', 'POST'])  # allow get and post requests
def login():
    # Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # login form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # Check if there is a requested redirect, and redirect to requested page if so
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Invalid login. Check your email and password.", "danger")
    return render_template('login.html', title="Login Page", form=form)


@app.route('/logout')
def logout():
    logout_user()  # provided by flask_login
    return redirect(url_for('home'))


def company_picture(form_picture):  # save a picture using randomized token
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/company_pics', picture_filename)  # joins paths to desired dir

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)  # resize the image using pillow

    i.save(picture_path)  # method of wtforms
    return picture_filename


@app.route('/account', methods=['GET', 'POST'])
@login_required  # requires login to access this page, goes to login route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = company_picture(form.picture.data)
            current_user.affiliation.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data  # these update the db as well, connected to by flask_login

        current_user.affiliation = form.affiliation.data

        db.session.commit()
        flash('Update successful.', 'success')
        return redirect(url_for('account'))  # avoid form input reload warning
    elif request.method == 'GET':
        form.affiliation.data = current_user.affiliation
        form.username.data = current_user.username  # autofill the form when the page is initially loaded
        form.email.data = current_user.email
    image_file = url_for('static', filename='company_pics/' + current_user.affiliation.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


def campaign_picture(form_picture):  # TODO connection
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/campaign_pics', picture_filename)  # joins paths to desired dir

    i = Image.open(form_picture)
    i.save(picture_path)  # method of wtforms
    return picture_filename


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        picture_file = None
        if form.image.data:
            picture_file = campaign_picture(form.image.data)

        post = Post(title=form.title.data, content=form.content.data, image_file=picture_file, author=current_user, affiliation=current_user.affiliation)
        db.session.add(post)
        db.session.commit()

        for recipient in form.recipients.data:
            db.session.add(PostRecipient(post_id=post.id, recipient_id=recipient.id))
        db.session.commit()

        flash('Post created.', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form, legend="Campaign Creator")


@app.route('/post/<int:post_id>')  # pass in post_id to the route, and use post_id in url
def post(post_id):
    post = Post.query.get_or_404(post_id)  # if does not exist, return 404 template TODO
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])  # pass in post_id to the route, and use post_id in url
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # abort the redirect
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title='Edit Post', form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # abort the redirect
    db.session.delete(post)  # delete post object
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')  # multiple decorators handled by the same function
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # load all posts from db and pass in to template
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route('/affiliation/<string:id>')
def affiliation_posts(id):
    page = request.args.get('page', 1, type=int)
    affiliation = Affiliation.query.filter_by(id=id).first_or_404()
    # load all posts from db and pass in to template
    posts = Post.query.filter_by(affiliation=affiliation)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('affiliation_posts.html', posts=posts, affiliation=affiliation)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='campaignmanager@gmail.com', recipients=[user.email])
    msg.body = f"""TO reset your password, click on the following link: 
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, you may ignore this email.
    """  # _external gives a non-localized link
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been set with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)  # get the user from the token
    if not user:
        flash('Invalid token', 'warning')
        return redirect(url_for('reset_request'))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()

            flash("Password reset successfully.", 'success')  # success: bootstrap class
            return redirect(url_for('login'))
        return render_template('reset_token.html', title="Reset Password", form=form)


@app.route('/unread_posts/')
def unread_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc())  # .paginate(page=page, per_page=5)
    filtered_posts = []
    for post in posts:
        for pr in PostRecipient.query.filter_by(post_id=post.id):
            if pr.recipient_id == current_user.affiliation.id:
                filtered_posts.append(post)
    return render_template('unread_posts.html', title="Unread Campaigns", posts=filtered_posts)
