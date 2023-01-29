from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_session import Session


# create the extension
import os
#diretório onde será enviado as imagens do banco
basedir = os.path.abspath(os.path.dirname(__file__))
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

#flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configuração do destino das imagens no banco
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif', 'svg', 'gif', 'webp'}
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)
patch_request_class(app)

#resolução do erro apos instalar o Werkzeug==0.16.0

#Tente o seguinte:
#após o pip install Werkzeug, entre na sua pasta do envoriment
#Ex do caminho: /Flask_curso/Site/meuenv/lib/python3.7/site-packages/flask_uploads.py

#Ao abrir o arquivo  flask_uploads.py voce muda a parte do import:
#from werkzeug import secure_filename,FileStorage
#Para:
#from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage



from loja.admin import rotas
from loja.produtos import rotas