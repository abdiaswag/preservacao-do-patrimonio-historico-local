from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)

    categoria = db.Column(db.String(100), nullable=False)

    imagem = db.Column(db.String(300))

    texto = db.Column(db.Text, nullable=False)