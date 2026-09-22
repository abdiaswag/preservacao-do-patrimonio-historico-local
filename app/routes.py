from flask import Blueprint, render_template, url_for, redirect, request
from .models import Materia,db


main = Blueprint("main", __name__)

#Homepage route
@main.route("/")
def index():

    materias = Materia.query.all()

    print(materias)

    return render_template(
        "index.html",
        materias=materias
    )


#Rota dinâmica para exibir uma matéria específica com base no ID fornecido
@main.route("/materia/<int:id>")
def materia(id):

    materia = Materia.query.get_or_404(id)

    return render_template(
        "materia.html",
        materia=materia
    )

# LISTAR MATÉRIAS
@main.route("/materias")
def listar_materias():

    materias = Materia.query.all()

    return render_template(
        "materias.html",
        materias=materias
    )


# CRIAR MATÉRIA
@main.route("/materias/criar", methods=["GET", "POST"])
def criar_materia():

    if request.method == "POST":

        titulo = request.form["titulo"]
        categoria = request.form["categoria"]
        imagem = request.form["imagem"]
        texto = request.form["texto"]

        nova_materia = Materia(
            titulo=titulo,
            categoria=categoria,
            imagem=imagem,
            texto=texto
        )

        db.session.add(nova_materia)
        db.session.commit()

        return redirect(url_for("main.listar_materias"))

    return render_template("cadastrar_materia.html")


# EDITAR MATÉRIA
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


# EXCLUIR MATÉRIA
@main.route("/materia/<int:id>/excluir", methods=["POST"])
def excluir_materia(id):

    materia = Materia.query.get_or_404(id)

    db.session.delete(materia)
    db.session.commit()

    return redirect(url_for("main.listar_materias"))

#Rota para a página de quiz
@main.route("/quiz")
def quiz():
    return render_template("quiz.html")
        