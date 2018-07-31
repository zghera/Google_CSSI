from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from models import User
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):              # taken from the webapp2 extrta session example
    def dispatch(self):                                 # override dispatch
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)       # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class WelcomeHandler(BaseHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if ((verification(email,password))):
            user = User.query().filter(User.email == email).fetch()[0]
            self.session['user']= user
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

class SignUpHandler(BaseHandler):
    def get (self):
        signup_template=JINJA_ENVIRONMENT.get_template('templates/signup.html')
        self.response.write(signup_template.render())
    def post(self):
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password = self.request.get('password')
        college = self.request.get('college')
        courses = self.request.get('courses') # list
        profile_pic = self.request.get('profile_pic')
        name = [first_name,last_name]
        new_user = User(name = name, email = email,
                        password = password, college = college,
                        courses = courses, profile_pic = profile_pic)
        new_user.put()
        self.session['user'] = new_user;
        user_dict={'user':new_user}

        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))

class DashboardHandler(BaseHandler):
    def get(self): #get rid of eventually or check to see if signed in
        user_dict={'user':self.session.get('user')}
        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))


class ProfileHandler(BaseHandler):
    def get (self):
        user_dict={'user':self.session.get('user')}
    def post(self):
        user_dict={'user':self.session.get('user')}
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/userprofile.html')

class CreateConnectHandler(BaseHandler):
    def get(self):
        createconnect_template = JINJA_ENVIRONMENT.get_template('templates/createconnect.html')


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/signup', SignUpHandler),
    ('/dashboard', DashboardHandler),
    ('/profile', ProfileHandler),
    ('/createconnect',CreateConnectHandler)
], debug=True)
