# -*- coding: utf8 -*-
__author__ = 'mir.lu'

# This file contains the REST endpoints for the user login & account management

import flask
from flask import flash
import zeeguu
import sqlalchemy.exc
from zeeguu.model import Language
from zeeguu.model import User

from zeeguu.account import acc


@acc.route("/my_account", methods=["GET"])
def my_account():
    if not flask.g.user:
        return flask.redirect(flask.url_for("gym.login"))

    return flask.render_template("my_account.html", user=flask.g.user)


@acc.route("/create_account", methods=("GET", "POST"))
def create_account():

    # A cool way of passing the arguments to the flask template
    template_arguments = dict (
         languages= Language.all(),
         native_languages = Language.native_languages(),
         default_learned= Language.default_learned()
    )

    # GET
    if flask.request.method == "GET":
        return flask.render_template("create_account.html", **template_arguments)

    # POST
    form = flask.request.form
    password = form.get("password", None)
    email = form.get("email", None)
    name = form.get("name", None)
    code = form.get("code", None)
    language = Language.find(form.get("language", None))
    native_language = Language.find(form.get("native_language", None))

    if not (code == "Kairo" or code == "unibe" or code == "rug"):
        flash("Invitation code is not recognized. Please contact us.")

    elif password is None or email is None or name is None:
        flash("Please enter your name, email address, and password")

    else:
        try:

            zeeguu.db.session.add(User(email, name, password, language, native_language))
            zeeguu.db.session.commit()
            user = User.authorize(email, password)
            flask.session["user"] = user.id
            return flask.redirect(flask.url_for("account.my_account"))

        except ValueError:
            flash("Username could not be created. Please contact us.")
        except sqlalchemy.exc.IntegrityError:
            flash(email + " is already in use. Please select a different email.")
        except:
            flash("Something went wrong. Please contact us.")
        finally:
            zeeguu.db.session.rollback()

    return flask.render_template("create_account.html", **template_arguments)


