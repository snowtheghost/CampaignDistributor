from flask import render_template, flash, redirect, url_for, redirect, request
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm
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


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/account')
@login_required  # requires login to access this page, goes to login route
def account():
    return render_template('account.html', title='Account')
