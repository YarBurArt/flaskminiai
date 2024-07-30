import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


data_dir = "data"

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not os.path.exists(os.path.join(project_dir, data_dir)):
    os.makedirs(os.path.join(project_dir, data_dir))

# Get the absolute path to the database file
db_path = os.path.join(project_dir, data_dir, "database.db")
app = Flask(__name__)
app.secret_key = "hueta123"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
print(f"\n\nsqlite:///{db_path}\n\n")
db = SQLAlchemy(app)
manager = LoginManager(app)


from logic import models, routers


with app.app_context():
    db.create_all()
