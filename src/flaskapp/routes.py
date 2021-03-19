from flask import render_template, flash, redirect, url_for
from flaskapp import app
from flaskapp.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created successfully.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Registration Form", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass  # TODO flash and redirect
        # if valid
            # flash("Login successful", "success")
            # return redirect(url_for('home'))
        # else:
            # flash("Invalid login. Check your username and password.", "danger")
    return render_template('login.html', title="Login Page", form=form)