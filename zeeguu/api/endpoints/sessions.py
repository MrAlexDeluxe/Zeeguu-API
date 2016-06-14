import flask
from flask import request

import zeeguu
from zeeguu.api import api
from zeeguu.api.route_wrappers import cross_domain, with_session
from zeeguu.model.session import Session
from zeeguu.model.user import User


@api.route("/session/<email>", methods=["POST"])
@cross_domain
def get_session(email):
    """
    If the email and password match,
    a new sessionId is created, and returned
    as a string. This sessionId has to be passed
    along all the other requests that are annotated
    with @with_user in this file
    """
    password = request.form.get("password", None)
    if password is None:
        flask.abort(400)
    user = User.authorize(email, password)
    if user is None:
        flask.abort(401)
    session = Session.for_user(user)
    zeeguu.db.session.add(session)
    zeeguu.db.session.commit()
    return str(session.id)


@api.route("/validate")
@cross_domain
@with_session
def validate():
    return "OK"


@api.route("/logout_session",
           methods=["GET"])
@cross_domain
@with_session
def logout():
    # Note: the gym uses another logout endpoint.

    try:
        session_id = int(request.args['session'])
    except:
        flask.abort(401)
    session = Session.query.get(session_id)

    # print "about to expire session..." + str(session_id)
    zeeguu.db.session.delete(session)
    zeeguu.db.session.commit()

    return "OK"