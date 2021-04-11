# This file is not intended for running, and only should be used for initial setup of db server side
import os

from flaskapp import db
from flaskapp.models import User, Post

if __name__ == "__main__":
    os.remove("flaskapp/site.db")
    db.create_all()  # creates all necessary tables

    # user = User(username="Test", email="test@test.com", password="test")  # create a User model and store as variable
    # db.session.add(user)  # adds the stored model to the database
    # db.session.commit()  # commits all changes to the database

    # User.query.all()  # query all users in list form
    # User.query.first()  # query and return the first user
    # User.query.filter_by(username="Test").all()  # query all users with the username "Test"
    # User.query.get(1)  # query user by unique id set as primary key

    # user.posts  # access an attribute or linked data to a user
    # user.id  # return the id of the user

    pass
