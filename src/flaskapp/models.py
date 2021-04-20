from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskapp import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):  # for login_manager
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # inherit from SQLite.Model and flask_login.UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliation.id'), nullable=True)
    admin = db.Column(db.Integer, nullable=False)
    provider = db.Column(db.Integer, nullable=False)
    distributor = db.Column(db.Integer, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.affiliation_id}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliation.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    recipients = db.relationship('PostRecipient', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.image_file})"


class Affiliation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='affiliation', lazy=True)
    users = db.relationship('User', backref='affiliation', lazy=True)
    employees = db.relationship('Employee', backref='affiliation', lazy=True)

    def __repr__(self):
        return f"{self.name}"


class PostRecipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('affiliation.id'), nullable=False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliation.id'), nullable=True)
