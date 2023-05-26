import uuid

import flask
import sirope
from flask import Blueprint, current_app, request, url_for
from flask_login import login_required, logout_user

from model.comentariodto import ComentarioDto
from model.tuitdto import TuitDto
from model.userdto import UserDto


def get_blprint():
 search = flask.blueprints.Blueprint("comentario", __name__,
 url_prefix="/comentario",
 template_folder="templates",
 static_folder="static")

 syrp = sirope.Sirope()

 return search, syrp

comentario_bp, srp = get_blprint()

@comentario_bp.route('/comentar', methods=["GET", "POST"])
def comentar():
     id = str(uuid.uuid4())
     twit_id = request.form['tuit_id']
     usr = UserDto.current_user()
     # Recuperar y guardar el nuevo mensaje
     if flask.request.method == "POST":
        message_txt = flask.request.form.get("edComentario")

        if not message_txt:
            flask.flash("No puedes subir un comentario vacio.")
            return flask.redirect(url_for('comentario.verComentarios', twit_id=twit_id))
        if len(message_txt) > 280:
            flask.flash("El tuit no puede superar los 280 caracteres.")
            return flask.redirect(url_for('comentario.verComentarios', twit_id=twit_id))
        srp.save(ComentarioDto(id,usr.email,message_txt,twit_id))

     return flask.redirect(url_for('comentario.verComentarios', twit_id=twit_id))

@comentario_bp.route('/verComentarios/<twit_id>', methods=["GET", "POST"])
def verComentarios(twit_id):
    oid = None
    for tuit in srp.load_all_keys(TuitDto):
        tuit_actual = srp.load(tuit)
        if tuit_actual.id == twit_id:
            oid = tuit
            break

    tuit_actual = srp.load(oid)
    comentarios = list(srp.load_all(ComentarioDto))
    sust = {
        "tuit": tuit_actual,
        "comentarios": comentarios,
    }

    return flask.render_template("comentarios.html", **sust)

@comentario_bp.route('/delete_comentario', methods=['POST','DELETE','GET'])
def delete_comentario():
    comentario_id = request.form['comentario_id']
    tuit_id = request.form['tuit_id']

    for comentario in srp.load_all_keys(ComentarioDto):
        comentario_actual = srp.load(comentario)
        if comentario_actual.id == comentario_id:
            srp.delete(comentario)
        else:
            print("Elemento no encontrado")

    return flask.redirect(url_for('comentario.verComentarios', twit_id=tuit_id))