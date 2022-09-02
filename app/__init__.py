from flask import Flask
import os
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(64)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app


