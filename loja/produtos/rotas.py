from flask import request, redirect, render_template, url_for, flash, session
from loja import app, db, photos
from .models import Marca, Categoria, Ad_produtos
from .forms import Addprodutos
import os, secrets

@app.route("/add_marca", methods = ['GET', 'POST'])
def add_marca():
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))

    if request.method == 'POST':
        getmarca = request.form.get('marca')
        marca = Marca(name=getmarca)
        db.session.add(marca)
        db.session.commit()
        flash(f'A marca {getmarca} foi adicionada com sucesso','success')
        return redirect(url_for('add_marca'))
    return render_template("produtos/add_marca.html", title='Cadastrar Marca', marcas='marcas')

@app.route("/add_categoria", methods = ['GET', 'POST'])
def add_cat():
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))

    if request.method == 'POST':
        getcategoria = request.form.get('categoria')
        categoria = Categoria(name=getcategoria)
        db.session.add(categoria)
        db.session.commit()
        flash(f'A categoria {getcategoria} foi adicionada com sucesso','success')
        return redirect(url_for('add_marca'))
    return render_template("produtos/add_marca.html", title='Cadastrar Categoria')

@app.route("/add_produto", methods=['GET','POST'])
def add_produto():
    if not session.get('email'):
        flash("Realize o login para acessar a página",'primary')
        return redirect(url_for('login'))
    
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)

    img_1= request.files.get('image_1')
    img_2= request.files.get('image_2')
    img_3= request.files.get('image_3')

    if request.method == 'POST':
        name = form.name.data
        color = form.color.data
        discount = form.discount.data
        discription = form.discription.data
        price = form.price.data
        stock = form.stock.data
        marca = request.form.get('marca')
        categoria = request.form.get('categoria')


        if img_1:
           image_1 = photos.save(img_1, name= secrets.token_hex(10)+'.')
        else:
            image_1 = ''
        if img_2:
           image_2 = photos.save(img_2, name= secrets.token_hex(10)+'.')
        else:
            image_2 = ''
        if img_3:    
           image_3 =photos.save(img_3, name= secrets.token_hex(10)+'.')
        else:
            image_3 = ''

        produto = Ad_produtos(name=name, color=color, discount=discount, discription=discription, price= price, stock=stock, marca_id = marca, categoria_id = categoria, img_1 = image_1, img_2 = image_2, img_3 = image_3 )
        db.session.add(produto)
        db.session.commit()
        flash('Produto {} foi adicionada com sucesso!'.format(name),'success')
    return render_template("produtos/add_produto.html", title='Cadastrar Produto', form = form, marcas = marcas, categorias = categorias)