from flask import request, redirect, render_template, url_for, flash, session
from loja import app, db, photos
from .models import Marca, Categoria, Ad_produtos
from .forms import Addprodutos
import os, secrets


@app.route('/')
def home():
    if not session.get('email'):
        #configuração da paginação
        page = request.args.get('page', 1, type=int)
        produtos = Ad_produtos.query.paginate(page=page, per_page=2)

        marcas = Marca.query.join(Ad_produtos , (Marca.id == Ad_produtos.marca_id)).all()
        categorias = Categoria.query.join(Ad_produtos, (Categoria.id == Ad_produtos.categoria_id))
        return render_template('produtos/index.html',categorias = categorias, marcas = marcas, produtos = produtos, title = 'Home')
    else:
        return redirect(url_for('admin'))

#Filtragem de produtos por categoria e marca

@app.route('/categoria/<int:id>')
def filter_cat(id):
    page = request.args.get('page', 1, type=int)
    produtos_filter_cat = Ad_produtos.query.filter(Ad_produtos.categoria_id == id).paginate(page=page, per_page=2)
    marcas = Marca.query.join(Ad_produtos , (Marca.id == Ad_produtos.marca_id)).all()
    categorias = Categoria.query.join(Ad_produtos, (Categoria.id == Ad_produtos.categoria_id)).all()
    return render_template('produtos/index.html', produtos = produtos_filter_cat, categorias = categorias, marcas = marcas)

@app.route('/filter/marca/<int:id>')
def filter_marca(id):
    page = request.args.get('page', 1, type=int)
    produtos_filter_marca = Ad_produtos.query.filter(Ad_produtos.marca_id == id).paginate(page=page, per_page=2)
    marcas = Marca.query.join(Ad_produtos , (Marca.id == Ad_produtos.marca_id)).all()
    categorias = Categoria.query.join(Ad_produtos, (Categoria.id == Ad_produtos.categoria_id)).all()
    return render_template('produtos/index.html', produtos = produtos_filter_marca, categorias = categorias, marcas = marcas)




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
        return redirect(url_for('add_cat'))
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
    img_4= request.files.get('image_4')
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
        if img_4:
           image_4 = photos.save(img_4, name= secrets.token_hex(10)+'.')
        else:
            image_4 = ''
        if img_3:    
           image_3 =photos.save(img_3, name= secrets.token_hex(10)+'.')
        else:
            image_3 = ''

        produto = Ad_produtos(name=name, color=color, discount=discount, discription=discription, price= price, stock=stock, marca_id = marca, categoria_id = categoria, img_1 = image_1, img_4 = image_4, img_3 = image_3 )
        db.session.add(produto)
        db.session.commit()
        flash('Produto {} foi adicionada com sucesso!'.format(name),'success')
    return render_template("produtos/add_produto.html", title='Cadastrar Produto', form = form, marcas = marcas, categorias = categorias)