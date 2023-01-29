from flask import render_template, request, url_for, redirect, flash, session
from loja.produtos.models import Ad_produtos, Marca, Categoria
from loja import app, db, photos
from .forms import RegistrationForm, LoginForm
from .models import user
from loja import bcrypt
import os, secrets


@app.route('/admin')
def admin(): 
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    produtos = Ad_produtos.query.all()
    return render_template('admin/index.html', title='Página Administrativa', produtos = produtos)

@app.route('/registrar', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        usuario = user(
            form.name.data,
            form.username.data,
            form.email.data,
            pw_hash)
        db.session.add(usuario)
        db.session.commit()
        flash('Obrigado por registrar {}!'.format(form.name.data),'primary')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, title='Registrar Usuários')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        usuario = user.query.filter_by(email = form.email.data).first()
        if usuario:
            if bcrypt.check_password_hash(usuario.password,form.password.data):
                session['email'] = form.email.data
                flash('Bem vindo {}! você está logado no sistema'.format(usuario.username),'primary')
                return redirect(request.args.get('next') or url_for("admin"))
            else:
                flash("NÃO FOI POSSÍVEL ACESSAR O SISTEMA",'danger')
        else:
            flash('Conta não existe','danger')
    return render_template('admin/login.html',form=form, title='Login')

@app.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('login'))

@app.route('/delete/produto/<int:id>', methods=['GET', 'POST'])
def delete_produto(id):
    produto = Ad_produtos.query.filter_by(id = id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('admin'))
