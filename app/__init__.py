from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'
CsrfProtect(app)

from app import views, models
