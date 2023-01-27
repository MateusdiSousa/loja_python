from flask_wtf.file import FileAllowed, FileField,FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators

class Addprodutos(Form):
    name = StringField('Nome: ',[validators.DataRequired()])
    color = TextAreaField('Cor: ',[validators.DataRequired()])
    discount = IntegerField('Desconto: ',[validators.DataRequired()])
    discription = TextAreaField('Descrição: ',[validators.DataRequired()])
    price = IntegerField('Preço: ',[validators.DataRequired()])
    stock = IntegerField('Estoque: ',[validators.DataRequired()])

    image_1 = FileField('Imagem 1: ',validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', 'psd'])])
    image_2 = FileField('Imagem 2: ',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', 'psd'])])
    image_3 = FileField('Imagem 3: ',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', 'psd'])])

    
    
    
