from flask import request, redirect, render_template, url_for, flash
from .forms import Addprodutos
from loja import app, db, photos
from .models import Marca, Categoria
import os

@app.route("/add_marca", methods = ['GET', 'POST'])
def add_marca():

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
    marcas = Marca.query.all()
    categorias = Categoria.query.all()
    form = Addprodutos(request.form)

    img_1= request.files.get('image_1')
    img_2= request.files.get('image_2')
    img_3= request.files.get('image_3')

    if request.method == 'POST':
        if img_1:
            photos.save(request.files.get('image_1'))
        if img_2:
            photos.save(request.files.get('image_2'))
        if img_3:    
            photos.save(request.files.get('image_3'))
        db.session.commit()
    return render_template("produtos/add_produto.html", title='Cadastrar Produto', form = form, marcas = marcas, categorias = categorias)