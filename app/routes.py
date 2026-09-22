from flask import Blueprint, current_app, render_template, url_for, redirect, request
from .models import Materia,db
import os


main = Blueprint("main", __name__)

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

    materias = Materia.query.all()

    return render_template(
        "materias.html",
        materias=materias
    )


# CRIAR 
@main.route("/materias/criar", methods=["GET", "POST"])
def criar_materia():

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
@main.route("/materia/<int:id>/editar", methods=["GET", "POST"])
def editar_materia(id):

    materia = Materia.query.get_or_404(id)

    if request.method == "POST":

        materia.titulo = request.form["titulo"]
        materia.categoria = request.form["categoria"]
        materia.imagem = request.form["imagem"]
        materia.texto = request.form["texto"]

        db.session.commit()

        return redirect(url_for("main.listar_materias"))

    return render_template(
        "editar_materia.html",
        materia=materia
    )


# EXCLUIR 
@main.route("/materia/<int:id>/excluir", methods=["POST"])
def excluir_materia(id):

    materia = Materia.query.get_or_404(id)

    db.session.delete(materia)
    db.session.commit()

    return redirect(url_for("main.listar_materias"))

#Rota quiz
@main.route("/quiz")
def quiz():
    return render_template("quiz.html")
        