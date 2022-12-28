from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "hueta123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://drevo:123@localhost/drevo'
db = SQLAlchemy(app)
manager = LoginManager(app)

from logic import models, routers

with app.app_context():
    db.create_all()
