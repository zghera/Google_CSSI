from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2
import os
import jinja2
import json


class User(ndb.Model):
    name = ndb.StringProperty(repeated=True) #list containing first_name and last_name
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    college = ndb.StringProperty(required=True)
    # courses = ndb.StringProperty(repeated=True) #list of courses/subjects
    courses = ndb.StringProperty(required=True)
    major = ndb.StringProperty(required=False)
    home_town = ndb.StringProperty(required=False)
    bio = ndb.StringProperty(required=False)
    profile_pic = ndb.StringProperty(required=False) #later use blobstore
    college_pic = ndb.StringProperty(required=False) #later use blobstore
    connect_events = ndb.StringProperty(repeated=True)
    friends = ndb.StringProperty(repeated=True)
    organizations = ndb.StringProperty(repeated=True)

class ConnectEvent(ndb.Model):
    time = ndb.StringProperty(required=True)
    location = ndb.StringProperty(repeated=True)
    users = ndb.StringProperty(repeated=True)
    #alert_time = ndb.StringProperty(required=True)

class FeedMessage(ndb.Model):
    post_type = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    connect_event = ndb.StringProperty(required=True)
    user = ndb.StringProperty(required=True)
    #alert_time = ndb.StringProperty(required=True)

class Course(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    users = ndb.StringProperty(repeated=True)

class Organization(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    users = ndb.StringProperty(repeated=True)
