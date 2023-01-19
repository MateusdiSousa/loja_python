from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/minha_loja"
# initialize the app with the extension
db = SQLAlchemy(app)

db.init_app(app)

from loja.admin import rotas