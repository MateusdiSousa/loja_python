from loja import db, app
from datetime import datetime

class Ad_produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.Text(20), nullable=False)
    discount = db.Column(db.Integer, default=0)
    discription = db.Column(db.String(180), nullable=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'),nullable=False)
    marca = db.relationship('Marca',backref=db.backref('marcas', lazy=True))

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'),nullable=False)
    categoria = db.relationship('Categoria',backref=db.backref('categorias', lazy=True))

    img_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    img_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    img_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Ad_produtos %r>' % self.name


class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique = True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique = True)

with app.app_context():
    db.create_all()