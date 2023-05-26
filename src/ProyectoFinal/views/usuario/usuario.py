import flask
import sirope
from flask import Blueprint, current_app
import flask_login
from flask_login import login_required, logout_user

from model.userdto import UserDto

from model.tuitdto import TuitDto

from model.comentariodto import ComentarioDto


def get_blprint():
 search = flask.blueprints.Blueprint("usuario", __name__,
 url_prefix="/usuario",
 template_folder="templates",
 static_folder="static")

 syrp = sirope.Sirope()

 return search, syrp

usuario_bp, srp = get_blprint()

@usuario_bp.route('/borrar_cuenta', methods=['POST'])
def borrar_cuenta():
    usr = UserDto.current_user()
    email_txt = usr.email
    list = srp.load_all_keys(UserDto)
    for user in list:
        user_actual = srp.load(user)
        if user_actual.email == email_txt:
            srp.delete(user)
            break

    #borramos los tuits y comentarios asociados a esa cuenta
    for tuit in srp.load_all_keys(TuitDto):
        tuit_actual = srp.load(tuit)
        if tuit_actual.usr == email_txt:
            srp.delete(tuit)

    for comentario in srp.load_all_keys(ComentarioDto):
        comentario_actual = srp.load(comentario)
        if comentario_actual.usr == email_txt:
            srp.delete(comentario)

    return flask.redirect('/')

@usuario_bp.route("/logear", methods=["GET","POST"])
def logear():

    email_txt = flask.request.form.get("edUser")
    password_txt = flask.request.form.get("edPassword")

    if not email_txt:
        usr = UserDto.current_user()
        if not usr:
            flask.flash("Introduce un usuario.")
            return flask.redirect("/usuario/login")
    else:
        if not password_txt:
            flask.flash("Introduce una contraseña.")
            return flask.redirect("/usuario/login")
        usr = UserDto.find(srp, email_txt)
        if not usr:
            flask.flash("El usuario introducido no existe.")
            return flask.redirect("/usuario/login")
        elif not usr.chk_password(password_txt):
            flask.flash("La contraseña es incorrecta.")
            return flask.redirect("/usuario/login")

        flask_login.login_user(usr)

    return flask.redirect("/")

@usuario_bp.route("/registroUser", methods=["GET","POST"])
def registroUser():
    email_txt = flask.request.form.get("edUser")
    password_txt = flask.request.form.get("edPassword")
    password2_txt = flask.request.form.get("edPassword2")

    if not email_txt:
            flask.flash("Introduce un nombre de usuario.")
            return flask.redirect("/usuario/registro")
    else:
        if len(email_txt) < 4 :
            flask.flash("El nombre de usuario debe tener al menos 4 caracteres.")
            return flask.redirect("/usuario/registro")
        if len(email_txt) > 64 :
            flask.flash("El nombre de usuario no debe superar los 64 caracteres.")
            return flask.redirect("/usuario/registro")
        if not password_txt:
            flask.flash("Introduce una contraseña.")
            return flask.redirect("/usuario/registro")
        if len(password_txt) < 8:
            flask.flash("La contraseña debe tener al menos 8 caracteres.")
            return flask.redirect("/usuario/registro")
        if len(password_txt) > 32:
            flask.flash("La contraseña no debe superar los 32 caracteres.")
            return flask.redirect("/usuario/registro")
        if not password2_txt:
            flask.flash("Confirma la contraseña.")
            return flask.redirect("/usuario/registro")
        if password2_txt!=password_txt:
            flask.flash("Las contraseñas no coinciden.")
            return flask.redirect("/usuario/registro")
        usr = UserDto.find(srp, email_txt)
        if usr:
            flask.flash("El nombre de usuario ya esta registrado")
            return flask.redirect("/usuario/registro")
        if not usr:
            usr = UserDto(email_txt, password_txt)
            srp.save(usr)

        flask_login.login_user(usr)

    return flask.redirect("/")

@usuario_bp.route('/logout', methods=["POST"])
@login_required
def logout():

    logout_user()
    return flask.redirect("/")

@usuario_bp.route('/registro')
def registro():
    return flask.render_template('registro.html')

@usuario_bp.route('/login')
def login():
    return flask.render_template('login.html')

@usuario_bp.route('/configuracion')
def configuracion():
    return flask.render_template('configuracion.html')


@usuario_bp.route('/')
def inicio():
    return flask.render_template('home.html')