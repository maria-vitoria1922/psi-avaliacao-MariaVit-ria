from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import database

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        flash("Implemente o cadastro com hash de senha.")

        if not nome or not email or not senha:
            flash('Preencha todos os campos!')
            return redirect(url_for('registro'))
        
        conexao = criar_conexao()

        usuario_existe = conexao.execute( "SELECT * FROM usuarios WHERE email = ?", (email,) ).fetchone()

        if usuario_existe:
            conexao.close()
            flash('Esse email já foi registrado!')
            return redirect(url_for("registro"))

        conexao.execute(""" INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?) """, (nome, email, senha))

        conexao.commit()
        conexao.close()

        flash('Registro foi realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        conexao = criar_conexao()
        usuario = conexao.execute( "SELECT * FROM usuarios WHERE email = ? AND senha = ?", (nome, senha) ).fetchone()
        conexao.close()

        flash('Email ou senha incorretos!')
        return redirect(url_for("login"))
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    flash("Implemente o logout com session.")
    return redirect(url_for("index"))
