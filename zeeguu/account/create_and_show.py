# -*- coding: utf8 -*-
from zeeguu.language.knowledge_estimator import SethiKnowledgeEstimator
from zeeguu.model.session import Session

__author__ = 'mir.lu'

# This file contains the REST endpoints for the user login & account management

import datetime
import flask
from flask import flash
import json
import zeeguu
import sqlalchemy.exc
from zeeguu.model.language import Language
from zeeguu.model.user import User

from zeeguu.account import acc


@acc.route("/create_account", methods=("GET", "POST"))
def create_account():
    # A cool way of passing the arguments to the flask template
    template_arguments = dict(
        languages=Language.all(),
        native_languages=Language.native_languages(),
        default_learned=Language.default_learned()
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

    if not (code == "Kairo" or code == "unibe" or code == "rug" or code == "42"):
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


@acc.route("/my_account", methods=["GET"])
def my_account():
    if not flask.g.user:
        return flask.redirect(flask.url_for("gym.login"))

    estimator = SethiKnowledgeEstimator(flask.g.user, flask.g.user.learned_language_id)

    graphs_caches = flask.g.user.GraphsCaches

    # check if graphs_caches exists and if it does, then check if it is up to date
    if graphs_caches is None or graphs_caches.activity_graph_cache_expire.date() < datetime.date.today():
        print "Generating new caches"

        # compute bookmark_counts_by_date
        year = datetime.date.today().year - 1  # get data from year 2015(if this year is 2016)
        month = datetime.date.today().month
        bookmarks_dict, dates = flask.g.user.bookmarks_by_date(datetime.datetime(year, month, 1))

        counts = []
        for date in dates:
            the_date = date.strftime('%Y-%m-%d')
            the_count = len(bookmarks_dict[date])
            counts.append(dict(date=the_date, count=the_count))

        bookmark_counts_by_date = json.dumps(counts)

        # compute learner_stats_data
        from zeeguu.model.learner_stats.learner_stats import compute_learner_stats
        learner_stats_data = compute_learner_stats(flask.g.user)

        # save generated graphs in DB as caches
        from zeeguu.model.graphs_caches import GraphsCaches
        current_datetime = datetime.datetime.now()

        # if graphs_caches doesnt exists then create it and then update it
        if graphs_caches is None:
            graphs_caches = GraphsCaches(' ', ' ', ' ', flask.g.user, None, None, None)

        # add/update activity_graph_cache to the graphs_caches
        graphs_caches.set_activity_graph_cache(str(bookmark_counts_by_date), current_datetime)
        # add/update line_graph_cache to the graphs_caches
        graphs_caches.set_line_graph_cache(str(learner_stats_data), current_datetime)

        # commit changes to DB
        zeeguu.db.session.add(graphs_caches)
        zeeguu.db.session.commit()
    else:
        print "Using caches"
        bookmark_counts_by_date = graphs_caches.activity_graph_cache
        learner_stats_data = graphs_caches.line_graph_cache

    s = Session.find_for_user(flask.g.user)
    zeeguu.db.session.add(s)
    zeeguu.db.session.commit()

    session_id = str(s.id).zfill(8)
    smartwatch_login_code = session_id[:4] + "-" + session_id[4:]

    print "Done loading parameters"

    return flask.render_template("my_account.html",
                                 user=flask.g.user,
                                 estimator=estimator,
                                 bookmark_counts_by_date=bookmark_counts_by_date,
                                 learner_stats_data=learner_stats_data,
                                 smartwatch_login_code=smartwatch_login_code)
