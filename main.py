from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from webapp2_extras import sessions
from google.appengine.api import mail
from models import *
# from models import User
# from models import ConnectEvent
# from models import UserConnectEvent
# from models import FeedMessage
# from models import Course
# from models import CourseRoster
# from models import Organization
# from models import OrganizationRoster

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def verification(email,password):
    #verify email and password
    #return true if exists
    #return false if account doesnt exist with given input
    return True


def email(connect_title,time,location,user_email,user_name,mail_subject):
    sender_address = "college.connect.cssi@gmail.com"
    mail_to = user_name+" "+"<"+user_email+">"
    mail_body = user_name+""":
        Your Connect Event, """+connect_title+""", is scheduled for
        """+time+""" at """+location+"""!

        Thank you for choosing College Connect!!
        The College Connect Team
        """
    mail_html = """
        <html><head></head><body>"""+user_name+""":<br>
        Your Connect Event, <b>"""+connect_title+"""</b>, is scheduled for
        """+time+""" at """+location+"""!<br>

        Thank you for choosing College Connect!!
        The College Connect Team
        </body></html>"""

    # mail_html = """
    #     <html><head></head><body>%(name)s :
    #     Your Connect Event,<b> %(title)s </b>, is scheduled for
    #     %(time)s at %(loc)s!
    #
    #     Thank you for choosing College Connect!!
    #     The College Connect Team
    #     </body></html>""" %
    #     {'name':user_name,'title':connect_title,'time':time,'loc':location}

    message = mail.EmailMessage(sender=sender_address,
                                subject = mail_subject,
                                to = mail_to,
                                body = mail_body,
                                html = mail_html)
    message.send()


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
            self.session['user']= email
            user_dict = {'user':user}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/dashboard.html').render(user_dict))
        else:
            pass
            #display error message in welcome


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

        # if not mail.is_email_valid(email):
        #     self.get()  # Show the form again.
        # else:
        #     confirmation_url = create_new_user_confirmation(email)
        #     sender_address = "college.connect.cssi@gmail.com"
        #     subject = 'Confirm your registration'
        #     body = """Thank you for creating an account!
        #     Please confirm your email address by clicking on the link below:
        #     {}""".format(confirmation_url)
        #     mail.send_mail(sender_address, email, subject, body)
        #
        # new_user = User(name = name, email = email,
        #                 password = password, college = college,
        #                 profile_pic = profile_pic, college_pic = "",
        #                 friends=[],)

        new_user.put()
        self.session['user'] = email

        user_dict={'user':new_user}

        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))

class DashboardHandler(BaseHandler):
    def get(self): #get rid of eventually or check to see if signed in
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        #user_key = User.query().filter(User.email == self.session.get('user')).get().key
        user_dict={'user':user}
        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')

        email("Party","7/31/18 4:00pm","The moon","abdinajka@gmail.com","Najib","Here is your email")

        self.response.write(dashboard_template.render(user_dict))

class FeedHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        feed_template = JINJA_ENVIRONMENT.get_template('templates/partials/feed.html')
        self.response.write(freinds_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]


class UserProfileHandler(BaseHandler):
    def get (self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        userprofile_template = JINJA_ENVIRONMENT.get_template('templates/userprofile.html')
        self.response.write(profile_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/userprofile.html')

class HostConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        hostconnect_template = JINJA_ENVIRONMENT.get_template('templates/hostconnect.html')
        self.response.write(hostconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        time = self.request.get('time')
        location = self.request.get('location')
        connect_title = self.request.get('title')
        course = self.request.get('course')
        new_ConnectEvent = ConnectEvent(time = time, location = location,
                                        connect_title = connect_title, course = course)
        new_ConnectEvent_key = new_ConnectEvent.put()
        users_keys = [user.key]
        new_UserConnectEvent = UserConnectEvent(users=users_keys,
                                                connect_event=new_ConnectEvent_key)
        new_UserConnectEvent.put()

class JoinConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        joinconnect_template = JINJA_ENVIRONMENT.get_template('templates/joinconnect.html')
        self.response.write(joinconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]



class FriendsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        friends_template = JINJA_ENVIRONMENT.get_template('templates/friends.html')
        self.response.write(freinds_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        # friend_added = self.request.get('friends_added') #if just one friend
        friends_added = self.request.get('friends_added')
        user.friends.extend(friend_added)

class CoursesHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        courses_template = JINJA_ENVIRONMENT.get_template('templates/courses.html')
        self.response.write(freinds_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]

class UpcomingConnectsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        friends_template = JINJA_ENVIRONMENT.get_template('templates/partials/upcomingconnects.html')
        self.response.write(freinds_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/signup', SignUpHandler),
    ('/dashboard', DashboardHandler),
    ('/feed',FeedHandler),
    ('/userprofile', UserProfileHandler),
    ('/hostconnect',HostConnectHandler),
    ('/joinconnect',JoinConnectHandler),
    ('/friends',FriendsHandler),
    ('/courses',CoursesHandler),
    ('/upcomingconnects',UpcomingConnectsHandler),
], debug=True, config=config)
