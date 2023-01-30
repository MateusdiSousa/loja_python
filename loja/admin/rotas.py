from flask import render_template, request, url_for, redirect, flash, session
from loja.produtos.models import Ad_produtos, Marca, Categoria
from loja import app, db, photos
from .forms import RegistrationForm, LoginForm, EditProduto
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

@app.route('/edit/produto/<int:id>', methods = ['GET', 'POST'])
def edit_produto(id):
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    
    form = EditProduto(request.form)
    marca = Marca.query.all()
    categoria = Categoria.query.all()
    #PEGANDO AS IMAGENS DO FORMS
    img_1= request.files.get('image_1')
    img_2= request.files.get('image_2')
    img_3= request.files.get('image_3')
    produto = Ad_produtos.query.filter_by(id = id).first()

    if request.method == 'POST':
        produto.name = form.name.data
        produto.color = form.color.data
        produto.discount = form.discount.data
        produto.discription = form.discription.data
        produto.price = form.price.data
        produto.stock = form.stock.data

        #Mandando as imagens do forms para o banco de dados, e para a 'images' do servidor
        produto.img_1 = photos.save(img_1, name= secrets.token_hex(10)+'.')
        if img_2:
            produto.img_2 = photos.save(img_2, name= secrets.token_hex(10)+'.')
        if img_3:
            produto.img_3 = photos.save(img_3, name= secrets.token_hex(10)+'.')

        produto.marca_id = request.form.get('marca')
        produto.categoria_id = request.form.get('categoria')

        db.session.commit()
        return redirect(url_for("admin"))
    return render_template('admin/edit.html',produto = produto, form = form, marcas = marca, categorias = categoria, title = 'Edição de Produto')

