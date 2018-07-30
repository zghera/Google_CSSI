from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from models import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if ((verification(email,password))):
            user = User.query().filter(User.email == email).fetch()[0]
            user_dict = {'user':user}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/dashboard.html').render(user_dict))
        else:
            pass
            #display error message in welcome

def verification(email,password):
    #verify email and password
    #return true if exists
    #return false if account doesnt exist with given input
    return True

class SignUpHandler(webapp2.RequestHandler):
    def get (self):
        signup_template=JINJA_ENVIRONMENT.get_template('templates/signup.html')
        self.response.write(signup_template.render())


class DashboardHandler(webapp2.RequestHandler):
    def post(self):
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password = self.request.get('password')
        college = self.request.get('college')
        courses = self.request.get('courses') # list
        profile_pic = self.request.get('profile_pic')
        new_user = User(name = first_name + last_name, email = email,
                        password = password, college = college,
                        courses = courses,) #profile_pic = profile_pic)
        new_user.put()
        user_dict={'user':new_user}

        self.response.write(JINJA_ENVIRONMENT.get_template('templates/dashboard.html').render(user_dict))

class ProfileHandler(webapp2.RequestHandler):
    def post(self):
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/newsfeed.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUpHandler),
    ('/dashboard', DashboardHandler),
    ('/profile', ProfileHandler),
], debug=True)
