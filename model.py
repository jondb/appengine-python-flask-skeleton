__author__ = 'jon'

from google.appengine.ext import db


class Status(db.Model):
    name = db.StringProperty(required=True)
    # Status is 0 for offline, 1 for online, and -1 for error condition.
    status = db.IntegerProperty(required=True)
    updated = db.DateTimeProperty(auto_now_add=True)
    error_text = db.TextProperty()
    latest = db.BooleanProperty(required=True)

    @classmethod
    def clear_latest(cls, name):
        status_query = cls.all()
        status_query.filter("name =", name)
        status_query.filter("latest =", True)
        for status in status_query.run(limit=50):
            status.latest = False
            status.put()

    @classmethod
    def update_status(cls, name, status, error_text=None):
        status = int(status)

        cls.clear_latest(name)

        status = cls(name=name, status=status, error_text=error_text, latest=True)
        status.put()
        return status

    @classmethod
    def summary(cls):
        status_gql = "SELECT * FROM Status where latest = TRUE order by name"
        status_query = db.GqlQuery(status_gql)
        names = [name for name in status_query.run(limit=1000)]
        return names

    def __repr__(self):
        return "<%s, %s, %s>" % (self.name, self.status, self.updated)