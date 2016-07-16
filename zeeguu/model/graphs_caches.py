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

    activity_graph_cache_expire = db.Column(db.DateTime)
    line_graph_cache_expire = db.Column(db.DateTime)
    piechart_cache_expire = db.Column(db.DateTime)

    def __init__(self, activity_graph_cache, line_graph_cache, piechart_cache, user, activity_graph_cache_expire, line_graph_cache_expire, piechart_cache_expire):
        self.user = user
        
        self.set_activity_graph_cache(activity_graph_cache, activity_graph_cache_expire)
        self.set_line_graph_cache(line_graph_cache, line_graph_cache_expire)
        self.set_piechart_cache(piechart_cache, piechart_cache_expire)

    def set_activity_graph_cache (self, activity_graph_cache, activity_graph_cache_expire):
        self.activity_graph_cache = activity_graph_cache
        self.activity_graph_cache_expire = activity_graph_cache_expire

    def set_line_graph_cache (self, line_graph_cache, line_graph_cache_expire):
        self.line_graph_cache = line_graph_cache
        self.line_graph_cache_expire = line_graph_cache_expire

    def set_piechart_cache (self, piechart_cache, piechart_cache_expire):
        self.piechart_cache = piechart_cache
        self.piechart_cache_expire = piechart_cache_expire