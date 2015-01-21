#import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.login import LoginManager
#from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.login_message = u"Please log in to access this page."
lm.refresh_view = "reauth"

from views import main