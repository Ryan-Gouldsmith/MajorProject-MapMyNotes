import logging
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_seasurf import SeaSurf

logging.basicConfig()

application = Flask(__name__)
application.config['TESTING'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mapmynotes'
database = SQLAlchemy(application)
# Better secret key. Help from this http://flask.pocoo.org/docs/0.10/quickstart/
application.secret_key = os.urandom(50)
application.config["root_url"] = "http://localhost:5000"
application.config['REDIRECT_URL_GOOGLE'] = "http://localhost:5000/oauthsubmit"

"""Blueprint reference http://flask.pocoo.org/docs/0.10/blueprints/
   Structure for larger applications modified http://flask.pocoo.org/docs/0.10/patterns/packages/
"""
application.config['secret_json_file'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client_secrets.json")

"""
When imports are at the top it can not access the database etc.
I found this resource which helped me to see they need to be further down.
http://stackoverflow.com/questions/15989928/importerror-when-importing-from-a-lower-module
"""
from controllers.homepage import homepage
from controllers.file_upload import fileupload
from controllers.metadata import metadata
from controllers.show_note import shownote
from controllers.oauth import oauth
from controllers.user import user
from controllers.view_all_notes import viewallnotes
from controllers.search import searchblueprint
from controllers.logout import logoutblueprint

application.register_blueprint(homepage)
application.register_blueprint(fileupload)
application.register_blueprint(metadata)
application.register_blueprint(shownote)
application.register_blueprint(oauth)
application.register_blueprint(user)
application.register_blueprint(viewallnotes)
application.register_blueprint(searchblueprint)
application.register_blueprint(logoutblueprint)

csrf = SeaSurf(application)
application.config['seasurf'] = csrf