from zeeguu import db
from zeeguu.model.bookmark import Bookmark


class WatchInteractionEvent(db.Model):
    __tablename__ = 'watch_interaction_event'
    __table_args__ = dict(mysql_collate='utf8_bin')

    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DateTime)

    bookmark_id=db.Column(db.Integer,db.ForeignKey('bookmark.id'),nullable=False)
    bookmark=db.relationship ("Bookmark")

    event_type_id=db.Column(db.Integer,db.ForeignKey('watch_event_type.id'),nullable=False)
    event_type=db.relationship ("WatchEventType")

    def __init__(self, event_type, bookmark_id, time):

        self.time = time
        self.bookmark_id = bookmark_id
        self.event_type = event_type

    def data_as_dictionary(self):
        return dict(
                bookmark_id= self.bookmark_id,
                time= self.time.strftime("%Y-%M-%dT%H:%M:%S"),
                event= self.event_type.name
        )

    def is_learned_event(self):
        return self.event_type.name == "learnedIt"

    def is_wrong_translation_event(self):
        return self.event_type.name == "wrongTranslation"

    @classmethod
    def events_for_bookmark(cls, bookmark):
        return cls.query.filter_by(bookmark_id=bookmark.id).all()

    @classmethod
    def events_for_bookmark_id(cls, bookmark_id):
        return cls.query.filter_by(bookmark_id=bookmark_id).all()

    @classmethod
    def events_for_user(cls, user):
        return cls.query.join(Bookmark).filter(Bookmark.user_id == user.id).all()






