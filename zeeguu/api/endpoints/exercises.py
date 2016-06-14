import traceback

from datetime import datetime

import zeeguu
from zeeguu.api import api
from zeeguu.api.route_wrappers import cross_domain, with_session
from zeeguu.api.json_result import json_result
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.exercise import Exercise
from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource


@api.route("/get_exercise_log_for_bookmark/<bookmark_id>", methods=("GET",))
@cross_domain
@with_session
def get_exercise_log_for_bookmark(bookmark_id):
    bookmark = Bookmark.query.filter_by(id=bookmark_id).first()

    exercise_log_dict = []
    exercise_log = bookmark.exercise_log
    for exercise in exercise_log:
        exercise_log_dict.append(dict(id = exercise.id,
                                      outcome = exercise.outcome.outcome,
                                      source = exercise.source.source,
                                      exercise_log_solving_speed = exercise.solving_speed,
                                      time = exercise.time.strftime('%m/%d/%Y')))

    return json_result(exercise_log_dict)


@api.route("/report_exercise_outcome/<exercise_outcome>/<exercise_source>/<exercise_solving_speed>/<bookmark_id>",
           methods=["POST"])
@with_session
def report_exercise_outcome(exercise_outcome,exercise_source,exercise_solving_speed,bookmark_id):
    """
    In the model parlance, an exercise is an entry in a table that
    logs the performance of an exercise. Every such performance, has a source, and an outcome.

    :param exercise_outcome: One of: Correct, Retry, Wrong, Typo, Too easy
    :param exercise_source: has been assigned to your app by zeeguu
    :param exercise_solving_speed: in milliseconds
    :param bookmark_id: the bookmark for which the data is reported
    :return:
    """

    try:
        bookmark = Bookmark.find(bookmark_id)
        new_source = ExerciseSource.find_by_source(exercise_source)
        new_outcome = ExerciseOutcome.find(exercise_outcome)

        if not new_source:
            return "could not find source"

        if not new_outcome:
            return "could not find outcome"

        exercise = Exercise(new_outcome,new_source,exercise_solving_speed, datetime.now())
        bookmark.add_new_exercise(exercise)
        zeeguu.db.session.add(exercise)
        zeeguu.db.session.commit()

        from zeeguu.language.knowledge_estimator import update_probabilities_for_word
        update_probabilities_for_word(bookmark.origin)
        return "OK"
    except :
        traceback.print_exc()
        return "FAIL"


