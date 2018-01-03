from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import flask
import json
import os

app = Flask(__name__)
quiz_dir = 'app/quizzes'

quizzes = {}
for quiz in os.listdir(quiz_dir):
    print 'Loading', quiz
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/wit'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'secret'

db = SQLAlchemy(app)

lm = LoginManager()

lm.init_app(app)

Bootstrap(app)

from app import controller
