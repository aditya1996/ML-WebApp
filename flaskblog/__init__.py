from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '0a749acc8c4c724a9e7c6cc846bf580a'

from flaskblog import routes