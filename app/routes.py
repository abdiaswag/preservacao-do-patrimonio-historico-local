from flask import Blueprint, current_app, render_template, url_for, redirect, request
from .models import Materia, Usuario,db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


main = Blueprint("main", __name__)

def somente_admin():
    if session.get("usuario_tipo") != "admin":
        return "Acesso negado. Apenas administradores podem acessar esta página.", 403

#Homepage 
@main.route("/")
def index():

    materias = Materia.query.all()

    print(materias)

    return render_template(
        "index.html",
        materias=materias
    )


#Rota dinâmica
@main.route("/materia/<int:id>")
def materia(id):

    materia = Materia.query.get_or_404(id)

    return render_template(
        "materia.html",
        materia=materia
    )

# LISTA
@main.route("/materias")
def listar_materias():

    acesso = somente_admin()
    if acesso:
        return acesso

    materias = Materia.query.all()

    return render_template(
        "materias.html",
        materias=materias
    )


# CRIAR 
@main.route("/materias/criar", methods=["GET", "POST"])
def criar_materia():

    acesso = somente_admin()
    if acesso:
        return acesso


    if request.method == "POST":

        titulo = request.form["titulo"]
        categoria = request.form["categoria"]
        imagem = request.files.get("imagem")
        texto = request.form["texto"]

        nome_imagem = None

        if imagem and imagem.filename:
            nome_imagem = imagem.filename

            caminho = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                nome_imagem
            )

            imagem.save(caminho)

        nova_materia = Materia(
            titulo=titulo,
            categoria=categoria,
            imagem=nome_imagem,
            texto=texto
        )

        db.session.add(nova_materia)
        db.session.commit()

        return redirect(url_for("main.listar_materias"))

    return render_template("cadastrar_materia.html")


# EDITAR 
@main.route("/materias/editar/<int:id>", methods=["GET", "POST"])
def editar_materia(id):

    materia = Materia.query.get_or_404(id)

    acesso = somente_admin()
    if acesso:
        return acesso

    if request.method == "POST":

        materia.titulo = request.form["titulo"]
        materia.categoria = request.form["categoria"]
        materia.texto = request.form["texto"]

        imagem = request.files.get("imagem")

        if imagem and imagem.filename:
            nome_imagem = imagem.filename
            caminho = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                nome_imagem
            )

            imagem.save(caminho)
            materia.imagem = nome_imagem


        db.session.commit()

        return redirect(url_for("main.listar_materias"))

    return render_template(
        "editar_materia.html",
        materia=materia
    )


# EXCLUIR 
@main.route("/materia/<int:id>/excluir", methods=["POST"])
def excluir_materia(id):

    acesso = somente_admin()
    if acesso:
        return acesso

    materia = Materia.query.get_or_404(id)

    db.session.delete(materia)
    db.session.commit()

    return redirect(url_for("main.listar_materias"))

#Rota quiz
@main.route("/quiz")
def quiz():
    return render_template("quiz.html")

#listar usuários
@main.route("/usuarios")
def listar_usuarios():

    acesso = somente_admin()
    if acesso:
        return acesso

    usuarios = Usuario.query.all()

    return render_template(
        "usuarios/listar.html",
        usuarios=usuarios
    )

#criar usuário
@main.route("/usuarios/criar", methods=["GET", "POST"])
def criar_usuario():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            tipo=tipo
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("usuarios/cadastrar.html")

#editar usuário
@main.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    acesso = somente_admin()
    if acesso:
        return acesso

    if request.method == "POST":

        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.tipo = request.form["tipo"]

        if request.form["senha"]:
            usuario.senha = generate_password_hash(
                request.form["senha"]
            )

        db.session.commit()

        return redirect(url_for("main.listar_usuarios"))

    return render_template(
        "usuarios/editar.html",
        usuario=usuario
    )

#excluir usuário
@main.route("/usuarios/excluir/<int:id>")
def excluir_usuario(id):

    acesso = somente_admin()
    if acesso:
        return acesso

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for("main.listar_usuarios"))

#login
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario and check_password_hash(
            usuario.senha,
            senha
        ):

            session["usuario_id"] = usuario.id
            session["usuario_tipo"] = usuario.tipo

            return redirect(url_for("main.index"))

        return "E-mail ou senha incorretos"

    return render_template("login.html")

#logout
@main.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.index"))

#area do usuário
@main.route("/usuario")
def area_usuario():
    if "usuario_id" not in session:
        return redirect(url_for("main.login"))

    usuario = Usuario.query.get_or_404(session["usuario_id"])
    return render_template("area_usuario.html", usuario=usuario)