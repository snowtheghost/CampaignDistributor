from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import os
from dotenv import load_dotenv

load_dotenv()  # env for secret key used in cookies

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # key for cookies
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # set the redirect to login route for login required routes
# login_manager.login_message_category = 'info'  # auto blue flash notification
login_manager.login_message = ""  # Don't show a message

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flaskapp import routes  # late import to first initialize db for routes
