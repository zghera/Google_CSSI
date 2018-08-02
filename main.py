from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from webapp2_extras import sessions
from models import *
from google.appengine.api import mail
from models import*
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

SCOPES = 'https://www.googleapis.com/auth/calendar'

store = oauth_file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = build('calendar', 'v3', http=creds.authorize(Http()))


def verification(email,password):
    users = User.query().fetch()
    for user in users:
        if user.email == email and user.password == password:
            return True
    return False


def create_calendar_event(summary,location,description,time_zone,start_time,end_time,attendee_email):
    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_dateTime,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end_dateTime,
        'timeZone': 'America/Los_Angeles',
      },
      'attendees': [
        {'email': attendee_email},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 6 * 60},
          {'method': 'popup', 'minutes': 60},
        ],
      },
    }

    event = service.events().insert(calendarId='college.connect.cssi@gmail.com', body=event).execute()
    event_link = event.get('htmlLink')
    event_id = event['id']
    return {'event_link':event_link,'event_id':event_id}


def update_calendar_event(event_id,summary,location,description,start_dateTime,end_dateTime,attendee_email):
    page_token = None
    while True:
      events = service.events().list(calendarId='college.connect.cssi@gmail.com', pageToken=page_token).execute()
      for event in events['items']:
        if event['id'] == event_id:
            the_event = event
      page_token = events.get('nextPageToken')
      if not page_token:
        break

    event_link = the_event.get('htmlLink')
    new_att_email_dict = {'email': attendee_email}
    event_attendees = the_event['attendees'].append(new_att_email_dict)
    updated_event = {'attendees': event_attendees}

    service.events().patch(calendarId='college.connect.cssi@gmail.com', eventId=event_id,
                            sendNotifications=True, body=updated_event).execute()

    return event_link


def email(type,event_id,connect_title,start_dateTime,end_dateTime,location,user_email,user_name,mail_subject):
    event_link = ""
    event_id = event_id

    if type == "host":
        event_dict = create_calendar_event(connect_title,location,"College Connect Session",start_dateTime,end_dateTime,user_email)
        event_link = event_dict['event_link']
        event_id = event_dict['event_id']

    elif type == "join":
        event_link = update_calendar_event(event_id,connect_title,location,"College Connect Session",start_dateTime,end_dateTime,user_email)

    sender_address = "college.connect.cssi@gmail.com"
    mail_to = user_name+" "+"<"+user_email+">"
    event_link = calendar_event()
    mail_body = user_name+""":
        Your Connect Event, """+connect_title+""", is scheduled for
        """+time+""" at """+location+"""!

        Thank you for choosing College Connect!!
        The College Connect Team
        """
    mail_html = """
        <html><head></head><body>"""+user_name+""":<br><br>
        Your Connect Event, <b>"""+connect_title+"""</b>, is scheduled for
        """+time+""" at """+location+"""!<br><br>

        View and accept your calendar invite at: """+event_link+"""<br><br>

        Thank you for choosing College Connect!!!<br>
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

    if type == "host":
        return event_id

def date_parser (date):
    index = date.find('/')
    month = date[:index]
    next_index = date.find('/',index+1)
    day = date[index+1:next_index]
    year = date[next_index+1:]
    return {'month':month,'day':day,'year':year}




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
        self.session['user']= ""
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        error_dict = {'error':""}
        self.response.write(welcome_template.render(error_dict))

    def post(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        email = self.request.get('email')
        password = self.request.get('password')

        if ((verification(email,password))):
            user = User.query().filter(User.email == email).fetch()[0]
            self.session['user']= email
            user_dict = {'user':user}
            self.redirect('/dashboard')
        else:
            error_dict = {'error':"error"}
            self.response.write(welcome_template.render(error_dict))
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
        courses = self.request.get('courses').split(", ") # list
        profile_pic = self.request.get('profile_pic')
        name = [first_name,last_name]

        new_user = User(name = name, email = email,
                        password = password, college = college,
                        profile_pic = profile_pic,
                        friends=[])

        # for course in Course.query().fetch():
        #     if (course.name == )


        new_user.put()
        self.session['user'] = email
        self.redirect('/dashboard')

class DashboardHandler(BaseHandler):

    def get(self): #get rid of eventually or check to see if signed in
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        all_posts_query = FeedMessage.query().order(-FeedMessage.date)
        all_posts = all_posts_query.fetch()
        user_dict = {'post': all_posts,'user':user}
        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))

        # # user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        # # email("Party","7/31/18 4:00pm","The moon","abdinajka@gmail.com","Najib","Here is your email")

    def post(self):
        post_content = self.request.get('status')

        if len(post_content)>0:
            new_post = FeedMessage(post=post_content)
            new_post.put()

        self.redirect('/dashboard')

class FeedHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        feed_template = JINJA_ENVIRONMENT.get_template('templates/partials/feed.html')
        self.response.write(feed_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]

class MessagesHandler(BaseHandler):
    def get (self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        messages_template = JINJA_ENVIRONMENT.get_template('templates/messages.html')
        self.response.write(messages_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}

class HostConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        hostconnect_template = JINJA_ENVIRONMENT.get_template('templates/hostconnect.html')
        self.response.write(hostconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        date = self.request.get('date')
        date_dict = date_parser(date)

        month = date_dict['month']
        day = date_dict['day']
        year = date_dict['year']

        time_st = self.request.get('time_st')
        time_end = self.request.get('time_end')

        start_dateTime = (year,month,day,0,0,0,0)
        end_dateTime = (year,month,day,0,1,0,0)

        location = self.request.get('location')
        connect_title = self.request.get('title')
        course = self.request.get('course')

        new_ConnectEvent = ConnectEvent(start_dateTime = start_dateTime,end_dateTime = end_dateTime,
         connect_location = location, connect_title = connect_title, course = course)
        new_ConnectEvent_key = new_ConnectEvent.put()
        users_keys = [user.key]
        new_UserConnectEvent = UserConnectEvent(users=users_keys,
                                                connect_event=new_ConnectEvent_key)
        new_UserConnectEvent.put()

        new_UserConnectEvent.event_id = email("host","",connect_title,time,location,user.email,user.name,"College Connect: Your Connect Event is Scheduled!")


class JoinConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        joinconnect_template = JINJA_ENVIRONMENT.get_template('templates/joinconnect.html')
        self.response.write(joinconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]


        email("join",connect_title,time,location,user.email,user.name,"College Connect: Your Connect Event is Scheduled!")

class FriendsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        friends_template = JINJA_ENVIRONMENT.get_template('templates/friends.html')
        self.response.write(friends_template.render(user_dict))

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
        self.response.write(courses_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]

class SettingsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        settings_template = JINJA_ENVIRONMENT.get_template('templates/settings.html')
        self.response.write(settings_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]

class AboutUsHandler(BaseHandler):
    def get(self):
        creators_template = JINJA_ENVIRONMENT.get_template('templates/aboutus.html')
        self.response.write(creators_template.render())

class ViewConnectsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        viewconnects_template = JINJA_ENVIRONMENT.get_template('templates/partials/viewconnects.html')
        self.response.write(viewconnects_template.render(user_dict))

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
    ('/feed', FeedHandler),
    ('/hostconnect', HostConnectHandler),
    ('/joinconnect', JoinConnectHandler),
    ('/friends', FriendsHandler),
    ('/courses', CoursesHandler),
    ('/aboutus', AboutUsHandler),
    ('/messages',MessagesHandler),
    ('/settings',SettingsHandler),
    ('/viewconnects',ViewConnectsHandler)
], debug=True, config=config)
