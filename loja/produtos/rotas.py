from flask import request, redirect, render_template, url_for, flash
from .forms import Addprodutos
from loja import app, db
from .models import Marca, Categoria

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

@app.route("/add_produto", methods = ['GET', 'POST'])
def add_produto():
    form = Addprodutos(request.form)
    
    return render_template("produtos/add_produto.html", title='Cadastrar Produto', form = form)