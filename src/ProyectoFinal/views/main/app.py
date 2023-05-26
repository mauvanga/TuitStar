# app.py
import redis
import flask
import sirope
import json
import flask_login

from model.comentariodto import ComentarioDto
from model.tuitdto import TuitDto
from model.userdto import UserDto
from views.comentario.comentario import comentario_bp
from views.like.like import like_bp
from views.tuit.tuit import tuit_bp

import datetime
from views.usuario.usuario import usuario_bp
import uuid


r = redis.Redis()

def create_app():
    lmanager = flask_login.LoginManager()
    fapp = flask.Flask(__name__)
    syrp = sirope.Sirope()

    fapp.config.from_file("config.json", load=json.load)
    lmanager.init_app(fapp)

    fapp.register_blueprint(comentario_bp)
    fapp.register_blueprint(like_bp)
    fapp.register_blueprint(tuit_bp)
    fapp.register_blueprint(usuario_bp)

    return fapp, lmanager, syrp

app, lm, srp = create_app()

@lm.user_loader
def user_loader(email):
    return UserDto.find(srp, email)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route('/', methods=["GET", "POST"])
def get_index():
    return flask.redirect('/tuit')


if __name__ == 'main':
    app.run()
#blueprints usuario y mensajes

#un archivo .py por cada blueprint y dentro funciones para diferentes rutas



