import uuid

import flask
import sirope
from flask import Blueprint, current_app, request, url_for, session
from flask_login import login_required, logout_user

from model.likedto import LikeDto
from model.tuitdto import TuitDto
from model.userdto import UserDto


def get_blprint():
 search = flask.blueprints.Blueprint("like", __name__,
 url_prefix="/like",
 template_folder="templates",
 static_folder="static")

 syrp = sirope.Sirope()

 return search, syrp

like_bp, srp = get_blprint()



@like_bp.route('/increase_like', methods=['POST','GET'])
def increase_like():
    twit_id = request.form['twit_id']
    usr = UserDto.current_user()
    encontrado = 0

    for tuit in srp.load_all_keys(TuitDto):
        tuit_actual = srp.load(tuit)
        if tuit_actual.id == twit_id:
            for like in srp.load_all_keys(LikeDto):
                like_actual = srp.load(like)
                if like_actual.tuit == twit_id:
                    if usr.email == like_actual.usr:
                        tuit_actual.quitarLike()
                        srp.save(tuit_actual)
                        srp.delete(like)
                        encontrado = 1
            if(encontrado==0):
                tuit_actual.darLike()
                srp.save(tuit_actual)
                srp.save(LikeDto(usr.email,twit_id))
    if (request.referrer.endswith("/tuit/mistuits")):
        return flask.redirect("/tuit/mistuits")
    elif("/comentario/verComentarios" in request.referrer):
        return flask.redirect(url_for('comentario.verComentarios', twit_id=twit_id))
    elif ("/tuit/buscarTuits" in request.referrer):
        palabra_clave = session.get('palabra_clave')
        print(palabra_clave)
        return flask.redirect(f"/tuit/buscarTuits?edBusqueda={palabra_clave}")
    else:
        return flask.redirect("/")
