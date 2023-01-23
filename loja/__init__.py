from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# create the extension

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/minha_loja"
#chave secreta para o flash
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# initialize the app with the extension
db = SQLAlchemy(app)

db.init_app(app)

bcrypt = Bcrypt(app)

from loja.admin import rotas