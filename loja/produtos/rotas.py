from flask import request, redirect, render_template, url_for, flash

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