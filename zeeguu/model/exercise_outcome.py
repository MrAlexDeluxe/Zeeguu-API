import sqlalchemy.orm

from zeeguu import db


class ExerciseOutcome(db.Model):
    __tablename__ = 'exercise_outcome'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    outcome=db.Column(db.String(255),nullable=False)

    TOO_EASY = 'Too easy'
    SHOW_SOLUTION = 'Show solution'
    CORRECT = 'Correct'
    WRONG = 'Wrong'

    def __init__(self,outcome):
        self.outcome = outcome


    @classmethod
    def find(cls, outcome):
        try:
            return cls.query.filter_by(
                outcome = outcome
            ).one()
        except  sqlalchemy.orm.exc.NoResultFound:
            return cls(outcome)