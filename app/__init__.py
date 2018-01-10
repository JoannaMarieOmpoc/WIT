from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/wit_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'secret'

db = SQLAlchemy(app)

lm = LoginManager()

lm.init_app(app)

Bootstrap(app)

from app import controller
