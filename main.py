<<<<<<< HEAD
# from google.appengine.ext  import ndb
=======
# from google.appengine.ext import ndb
>>>>>>> 2278993dcfcf1c73bab3797a3262c62b7447b070
# import webapp2
# import jinja2
# import os

import logging
from flask import Flask

# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)
#
# class Main(webapp2.RequestHandler):
#     def get(self):
#         login_template = JINJA_ENVIRONMENT.get_template('templates/template.html')
#         self.response.write(login_template.render())
#
# class UserProfile(webapp2.RequestHandler):

app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello"

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=4000)
=======
    app.run(host='0.0.0.0')
>>>>>>> 2278993dcfcf1c73bab3797a3262c62b7447b070
