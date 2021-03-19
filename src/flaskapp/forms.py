# User input forms using flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
