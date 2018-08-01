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
    #courses = ndb.KeyProperty(Course, repeated=True) #list of courses/subjects
    #courses = ndb.StringProperty(required=True)
    major = ndb.StringProperty(required=False)
    home_town = ndb.StringProperty(required=False)
    bio = ndb.StringProperty(required=False)
    #connect_events = ndb.KeyProperty(ConnectEvent, repeated=True)
    #connect_events = ndb.StringProperty(repeated=True)
    friends = ndb.StringProperty(repeated=True)
    profile_pic = ndb.StringProperty(required=True) #later use blobstore
    college_pic = ndb.StringProperty(required=True) #later use blobstore
    #organizations = ndb.StringProperty(repeated=True)

class ConnectEvent(ndb.Model):
    time = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    #users = ndb.StringProperty(repeated=True)
    alert_time = ndb.StringProperty(required=True)

class UserConnectEvent(ndb.Model):
    users = ndb.KeyProperty(User,repeated=True)
    connect_event = ndb.KeyProperty(ConnectEvent)

class FeedMessage(ndb.Model):
    post = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(kind=User, required=False)

class Course(ndb.Model):
    name = ndb.StringProperty(required=True)
    #description = ndb.StringProperty(required=True)

class CourseRoster(ndb.Model):
    user = ndb.KeyProperty(User)
    course = ndb.KeyProperty(Course)


class Organization(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class OrganizationRoster(ndb.Model):
    user = ndb.KeyProperty(User)
    organization = ndb.KeyProperty(Organization)
