from wtforms import Form, BooleanField, StringField, PasswordField, validators

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
        