import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Justin Chan',
        'title': ' Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Example Author',
        'title': 'Post 2',
        'content': 'Example post content',
        'date_posted': 'April 21, 2018'
    }
]


# Specifies the web directory, in this case, the root/homepage
@app.route('/')
@app.route('/home')  # multiple decorators handled by the same function
def home():
    return render_template('home.html', posts=posts)


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
        hashed_password = \
            bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash password and decode hash to string
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # Add created model to db and commit
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully.", 'success')  # success: bootstrap class
        return redirect(url_for('login'))
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


def save_picture(form_picture):  # save a picture using randomized token
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)  # joins paths to desired dir

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
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data  # these update the db as well, connected to by flask_login
        db.session.commit()
        flash('Update successful.', 'success')
        return redirect(url_for('account'))  # avoid form input reload warning
    elif request.method == 'GET':
        form.username.data = current_user.username  # autofill the form when the page is initially loaded
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
