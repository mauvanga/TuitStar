import uuid

import flask
import sirope
from flask import Blueprint, current_app, request, session

from model.comentariodto import ComentarioDto
from model.tuitdto import TuitDto
from model.userdto import UserDto


def get_blprint():
 search = flask.blueprints.Blueprint("tuit", __name__,
 url_prefix="/tuit",
 template_folder="templates",
 static_folder="static")

 syrp = sirope.Sirope()

 return search, syrp

tuit_bp, srp = get_blprint()

@tuit_bp.route('/', methods=["GET", "POST"])
def get_index():
     id = str(uuid.uuid4())
     usr = UserDto.current_user()
     # Recuperar y guardar el nuevo mensaje
     if flask.request.method == "POST":
        message_txt = flask.request.form.get("edMessage")
        if not message_txt:
            flask.flash("No puedes subir un tuit vacio.")
            return flask.redirect("/")
        if len(message_txt) > 280:
            flask.flash("El tuit no puede superar los 280 caracteres.")
            return flask.redirect("/")
        srp.save(TuitDto(id,usr.email,message_txt))
     # Visualizarlos todos
     messages_list = list(srp.load_all(TuitDto))
     comentarios = list(srp.load_all(ComentarioDto))

     sust = {
         "usr": usr,
         "messages_list": messages_list,
         "comentarios": comentarios,
     }

     return flask.render_template("home.html", **sust)


@tuit_bp.route('/mistuits', methods=["GET", "POST"])
def verMisTuits():
    tuits = list(srp.load_all(TuitDto))
    comentarios = list(srp.load_all(ComentarioDto))
    mis_tuits = [tuit for tuit in tuits if tuit.usr == UserDto.current_user().email]
    sust = {
        "tuits": mis_tuits,
        "comentarios": comentarios,
    }

    return flask.render_template("mistuits.html", **sust)

@tuit_bp.route('/delete_twit', methods=['POST','GET','DELETE'])
def delete_twit():
    twit_id = request.form['twit_id']

    for tuit in srp.load_all_keys(TuitDto):
        tuit_actual = srp.load(tuit)
        if tuit_actual.id == twit_id:
            srp.delete(tuit)
        else:
            print("Elemento no encontrado")

    if(request.referrer.endswith("/tuit/mistuits")):
        return flask.redirect("/tuit/mistuits")
    elif("/tuit/buscarTuits" in request.referrer):
        palabra_clave = session.get('palabra_clave')
        return flask.redirect(f"/tuit/buscarTuits?edBusqueda={palabra_clave}")
    else:
        return flask.redirect("/")


@tuit_bp.route('/buscarTuits', methods=['POST','GET'])
def buscartuits():
    palabra_clave = session.get('palabra_clave')
    if flask.request.form.get("edBusqueda"):
        palabra_clave = flask.request.form.get("edBusqueda")
        session['palabra_clave'] = palabra_clave

    tuits_encontrados = []

    for tuit in srp.load_all(TuitDto):
        if palabra_clave.lower() in tuit.msg.lower():
            tuits_encontrados.append(tuit)

    return flask.render_template('tuitsbuscados.html', tuits=tuits_encontrados, palabra_clave=palabra_clave)
