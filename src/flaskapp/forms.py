# User input forms using flask_wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskapp.models import User

MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 20

MIN_PASSWORD_LENGTH = 8


# Class for registration forms inheriting from FlaskForm
class RegistrationForm(FlaskForm):
    # Assign each variable to a validated field
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # query db for user with same username
        if user:  # if there is a user with the username, raise validation error
            raise ValidationError('Username taken.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()  # query db for user with same email
        if email:  # if there is a user with the email, raise validation error
            raise ValidationError('Email already in use.')  # this error is connected to wtforms and shows


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()  # query db for user with same username
            if user:  # if there is a user with the username, raise validation error
                raise ValidationError('Username taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()  # query db for user with same email
            if email:  # if there is a user with the email, raise validation error
                raise ValidationError('Email already in use.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

