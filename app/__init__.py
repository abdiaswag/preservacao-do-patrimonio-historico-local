import os
from flask import Flask
from .models import db



def create_app():

        app = Flask(__name__)

        app.config["SECRET_KEY"] = "secret_key"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder,"uploads")
        db.init_app(app)

        from .routes import main
        app.register_blueprint(main)

        with app.app_context():
            db.create_all()

        return app