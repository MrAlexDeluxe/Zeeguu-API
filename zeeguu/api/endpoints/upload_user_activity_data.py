import flask
from flask import request
from zeeguu import db

from zeeguu.api import api
from zeeguu.api.route_wrappers import cross_domain, with_session
from zeeguu.model.user_activitiy_data import UserActivityData


@api.route("/upload_user_activity_data", methods=["POST"])
@cross_domain
@with_session
def upload_user_activity_data():
    """
    The user needs to be logged in, so the event
    referst to themselves. Thus there is no need
    for submitting a user id.

    There are four elements that can be submitted for
    an user activity event. Within an example they are:

            time: '2016-05-05T10:11:12',
            event: "User Looked at Article",
            value: "300s",
            extra_data: "{article_source: 2, ...}"

    All these four elements have to be submitted as POST
    arguments

    :param self:
    :return: OK if all went well
    """
    print request.form

    time = request.form['time']
    event = request.form['event']
    value = request.form['value']
    extra_data = request.form['extra_data']

    new_entry = UserActivityData(flask.g.user,
                                 time,
                                 event,
                                 value,
                                 extra_data)
    db.session.add(new_entry)
    db.session.commit()
    return "OK"


