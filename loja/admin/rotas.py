from flask import render_template, request, url_for, redirect, flash, session

from loja import app, db
from .forms import RegistrationForm
from .models import User
from loja import bcrypt

@app.route('/')
def home():
    return render_template('admin/index.html', title='Página Administrativa')

@app.route('/registrar', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        email_hash =  bcrypt.generate_password_hash(form.email.data)
        user = User(
            form.name.data,
            form.username.data,
            email_hash,
            pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Obrigado por registrar {{form.name.data}}!','primary')
        return redirect(url_for('home'))
    return render_template('admin/registrar.html', form=form, title='Registrar Usuários')