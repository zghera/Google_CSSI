from google.appengine.ext import ndb
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Main(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/template.html')
        self.response.write(login_template.render())

class UserProfile(webapp2.RequestHandler):
