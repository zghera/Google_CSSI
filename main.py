from google.appengine.ext import ndb
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

        login = self.request.get('login')
        signup = self.request.get('signup')

        if login:
            user = self.request.get('email')
            password = self.request.get('password')
            user_login = User.query().filter(User.email == user and User.password == password).fetch()

class SignUpHandler(webapp2.RequestHandler):
    def post(self):
        signup_template = JINJA_ENVIRONMENT.get_template('templates/signup.html')
        self.response.write(signup_template.render())

        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password = self.request.get('password')
        college = self.request.get('college')
        courses = self.request.get('courses') #this is a list
        profile_pic = self.request.get('profile_pic')
        new_account = User(name = first_name + last_name, email = email, #create a new User database
                        password = password, college = college,
                        courses = courses, profile_pic = profile_pic)
        new_account.put()

class NewsFeedHandler(webapp2.RequestHandler):
    def post(self):
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/newsfeed.html')

class ProfileHandler(webapp2.RequestHandler):
    def post(self):
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/newsfeed.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUpHandler),
    ('/newsfeed', NewsFeedHandler),
    ('/profile', ProfileHandler),
], debug=True)
