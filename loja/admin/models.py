from loja import db , app

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(25), nullable =False, unique = True)
    email = db.Column(db.String(60), nullable=False,unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email 
        self.password = password

with app.app_context():
    db.create_all()