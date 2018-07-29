from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import webapp2
import os
import jinja2
import json
from random import shuffle
from models import Gif
import HTMLParser
import time
from models import Gif

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Welcome(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/template.html')
        self.response.write(login_template.render())

class Dashboard(webapp2.RequestHandler):


app = webapp2.WSGIApplication([
    ('/', Welcome),
    ('/',d),
], debug=True)
