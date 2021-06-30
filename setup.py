import os

from flaskapp import bcrypt, db
from flaskapp.models import User

"""
try:
    os.remove('flaskapp/site.db')
except:
    pass
"""

db.create_all()
db.session.commit()

hashed_password = \
    bcrypt.generate_password_hash("temporary").decode('utf-8')
user = User(username="Admin", email="temporary@mail.com",
            password=hashed_password, admin=1,
            affiliation=None,
            provider=0, distributor=0)

db.session.add(user)
db.session.commit()
