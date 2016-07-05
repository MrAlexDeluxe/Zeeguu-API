from zeeguu import db


class GraphsCaches(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'graphs_caches'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    user = db.relationship("User", backref=db.backref("GraphsCaches", uselist=False))

    activity_graph_cache = db.Column(db.String(2500))
    line_graph_cache = db.Column(db.String(1800))
    piechart_cache = db.Column(db.String(450))

    def __init__(self, activity_graph_cache, line_graph_cache, piechart_cache, user):
        self.activity_graph_cache = activity_graph_cache
        self.line_graph_cache = line_graph_cache
        self.piechart_cache = piechart_cache
        self.user = user

    def set_activity_graph_cache (self, activity_graph_cache):
        self.activity_graph_cache = activity_graph_cache

    def set_line_graph_cache (self, line_graph_cache):
        self.line_graph_cache = line_graph_cache

    def set_piechart_cache (self, piechart_cache):
        self.piechart_cache = piechart_cache