from flask import render_template, request, url_for, redirect, flash, session

from loja import app, db

@app.route('/')
def home():
    return '<h1> Olá mundo </h1>'

@app.route('/registrar')
def registrar():
    return render_template('admin/registrar.html', title='Registrar Usuário')