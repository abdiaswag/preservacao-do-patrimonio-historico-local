from flask import Blueprint, render_template
from .models import Materia,db


main = Blueprint("main", __name__)


@main.route("/")
def index():

    materias = Materia.query.all()

    print(materias)

    return render_template(
        "index.html",
        materias=materias
    )


@main.route("/materia/<int:id>")
def materia(id):

    materia = Materia.query.get_or_404(id)

    return render_template(
        "materia.html",
        materia=materia
    )

@main.route("/criar-materias")
def criar_materias():

    materia1 = Materia(
        titulo="Base Aérea e Trampolim da Vitória",
        categoria="Segunda Guerra Mundial",
        imagem="base-aerea.jpg",
        texto="Durante a Segunda Guerra Mundial, Parnamirim teve grande importância estratégica devido à sua localização."
    )

    materia2 = Materia(
        titulo="Barreira do Inferno",
        categoria="Ciência e Tecnologia",
        imagem="barreira-inferno.jpg",
        texto="O Centro de Lançamento da Barreira do Inferno foi criado em 1965 e possui grande importância para a história espacial brasileira."
    )

    materia3 = Materia(
        titulo="História de Parnamirim",
        categoria="História Local",
        imagem="parnamirim.webp",
        texto="Parnamirim possui uma história marcada pela aviação, pelo desenvolvimento urbano e por importantes acontecimentos do Rio Grande do Norte."
    )

    db.session.add(materia1)
    db.session.add(materia2)
    db.session.add(materia3)

    db.session.commit()

    return "Matérias cadastradas com sucesso!"

@main.route("/limpar")
def limpar():
    Materia.query.delete()
    db.session.commit()

    return "Todas as matérias foram deletadas!"

@main.route("/quiz")
def quiz():
    return render_template("quiz.html")
        