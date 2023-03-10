from flask import render_template, request, url_for, redirect, flash, session, current_app
from loja.produtos.models import Ad_produtos, Categoria, Marca
from loja import app, db, photos
from .forms import RegistrationForm, LoginForm
from ..produtos.forms import Addprodutos
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
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    produto = Ad_produtos.query.filter_by(id = id).first()
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit/produto/<int:id>', methods = ['GET', 'POST'])
def edit_produto(id):
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    
    form = Addprodutos(request.form)
    marca = Marca.query.all()
    categoria = Categoria.query.all()
    #PEGANDO AS IMAGENS DO FORMS
    
    produto = Ad_produtos.query.filter_by(id = id).first()
    img_1= request.files.get('image_1')
    img_2= request.files.get('image_2')
    img_3= request.files.get('image_3')

    

    if request.method == 'POST':
        produto.name = form.name.data
        produto.color = form.color.data
        produto.discount = form.discount.data

        produto.marca_id = request.form.get('marca')
        produto.categoria_id = request.form.get('categoria')

        produto.discription = form.discription.data
        produto.price = form.price.data
        produto.stock = form.stock.data

        #atualização das imagens do banco dados e do servidor, (agora ocorre apenas a troca de imagens ao inves de sempre adicionar uma imagem nova)
        #obs: foi necessário utilizar a biblioteca os, extensão do flask 'current_app' e a variavel photos 
        if img_1:
            try:

                os.unlink(os.path.join(current_app.root_path,'static/images/'+produto.img_1))
                produto.img_1 = photos.save(img_1, name= secrets.token_hex(10)+'.')
            except:
                produto.img_1 = photos.save(img_1, name= secrets.token_hex(10)+'.')

        if img_2:
            try:
                os.unlink(os.path.join(current_app.root_path,'static/images/'+produto.img_2))
                produto.img_2 = photos.save(img_2, name= secrets.token_hex(10)+'.')
            except:
                produto.img_2 = photos.save(img_2, name = secrets.token_hex(10)+'.')
        
        if img_3:
            try:
                os.unlink(os.path.join(current_app.root_path,'static/images/'+produto.img_3))
                produto.img_3 = photos.save(img_3, name= secrets.token_hex(10)+'.')
            except:
                produto.img_2 = photos.save(img_3, name = secrets.token_hex(10)+'.')
                
        db.session.commit()
        flash('Produto {} foi atualizado com sucesso'.format(produto.name),'primary')
        return redirect(url_for("admin"))
    

    #mostrar o valor atual das várias de textarea no forms
    form.color.data = produto.color
    form.discription.data = produto.discription
    return render_template('admin/edit.html',produto = produto, form = form, marcas = marca, categorias = categoria, title = 'Edição de Produto')

@app.route('/categoria')
def categoria():
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    categoria = Categoria.query.order_by(Categoria.id).all()

    return render_template('admin/marca.html', title='Página Categoria', categorias = categoria)

@app.route('/att_categoria<int:id>', methods=['GET', 'POST'])
def att_categoria(id):
    if not session.get("email"):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    categoria = Categoria.query.filter_by(id = id).first()
    if request.method == 'POST':
        categoria.name = request.form.get('categoria')
        db.session.commit()
        flash('A categoria foi atualizada','success')
        return redirect(url_for('categoria'))
    return render_template("admin/att_categoria_marca.html", categoria = categoria, )

@app.route('/del_categoria/<int:id>', methods=['GET', 'POST'])
def del_cat(id):
    if not session.get("email"):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    categoria = Categoria.query.filter_by(id = id).first()
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route('/marcas')
def marcas():
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    marcas = Marca.query.order_by(Marca.id).all()

    return render_template('admin/marca.html', title='Página Marcas', marcas = marcas)

@app.route('/att_marca/<int:id>', methods = ['GET', 'POST'])
def att_marca(id):
    if not session.get("email"):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    marcas =  Marca.query.filter_by(id = id).first()
    if request.method == 'POST':
        att_marca = request.form.get('marca')
        marcas.name = att_marca
        db.session.commit()
        flash('A Marca foi atualizada','success')
        return redirect(url_for('marcas'))
    return render_template("admin/att_categoria_marca.html",title = 'Atualização de Marca', marcas = marcas )

@app.route('/del_marca/<int:id>', methods=['GET', 'POST'])
def del_marca(id):
    if not session.get("email"):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    marca = Marca.query.filter_by(id = id).first()
    db.session.delete(marca)
    db.session.commit()
    return redirect(url_for('marcas'))
