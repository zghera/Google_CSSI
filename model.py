from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    age = ndb.IntegerProperty(required=True)
    college = ndb.StringProperty(required=True)
    courses = ndb.StringProperty(repeated=True) #list of courses/subjects and (un)declared major
