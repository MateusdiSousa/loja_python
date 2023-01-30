from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from flask_wtf.file import FileAllowed, FileField,FileRequired
from loja import photos

class RegistrationForm(Form):
    name = StringField('Nome Completo', [validators.Length(min=4, max=45)])
    username = StringField('Nome de Usuário', [validators.Length(min=4, max=25)])
    email = StringField('Endereço de Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Nova senha', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senhas não são iguais')
    ])
    confirm = PasswordField('Repita a senha')


class LoginForm(Form):
        email = StringField("Email:", [validators.Length(min=6, max=35)])
        password = PasswordField("Senha", [validators.DataRequired()])
        
class EditProduto(Form):
    name = StringField('Nome do Produto', [validators.DataRequired()])
    color = TextAreaField("Cor do Produto:", [validators.DataRequired()])
    discount = IntegerField("Desconto do Produto",[validators.DataRequired()])
    discription = TextAreaField('Descrição: ',[validators.DataRequired()])
    price = IntegerField('Preço: ',[validators.DataRequired()])
    stock = IntegerField('Estoque: ',[validators.DataRequired()])

    image_1 = FileField('Imagem 1: ',validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', '.jfif'])])
    image_2 = FileField('Imagem 2: ',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', '.jfif'])])
    image_3 = FileField('Imagem 3: ',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif','webp','svg', 'tiff', 'bmp', '.jfif'])])