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
    major = ndb.StringProperty(required=False)
    home_town = ndb.StringProperty(required=False)
    bio = ndb.StringProperty(required=False)
    friends = ndb.StringProperty(repeated=True)
    profile_pic = ndb.StringProperty(required=False) #later use blobstore
    # college_pic = ndb.StringProperty(required=True) #later use blobstore
    #organizations = ndb.StringProperty(repeated=True)

class Course(ndb.Model):
    name = ndb.StringProperty(required=True)
    #description = ndb.StringProperty(required=True)

class CourseRoster(ndb.Model):
    user = ndb.KeyProperty(User)
    course = ndb.KeyProperty(Course)

class ConnectEvent(ndb.Model):
    created_dateTime = ndb.DateTimeProperty(auto_now_add = True, auto_now=False)
    start_dateTime = ndb.DateTimeProperty(required = True)
    end_dateTime = ndb.DateTimeProperty(required = True)
    connect_location = ndb.GeoPtProperty(required=True)
    connect_title = ndb.StringProperty(required=True)
    course = ndb.KeyProperty(Course)
    event_id = ndb.StringProperty(required=False)

class UserConnectEvent(ndb.Model):
    users = ndb.KeyProperty(User,repeated=True)
    connect_event = ndb.KeyProperty(ConnectEvent)

class FeedMessage(ndb.Model):
    post = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # user = ndb.KeyProperty(kind=User, required=False)

class Organization(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class OrganizationRoster(ndb.Model):
    user = ndb.KeyProperty(User)
    organization = ndb.KeyProperty(Organization)
