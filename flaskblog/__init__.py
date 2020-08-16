from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = '0a749acc8c4c724a9e7c6cc846bf580a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["MONGO_URI"] = "mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/datasets?retryWrites=true&w=majority"


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flaskblog import routes