from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
import os


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mapmynotes'
database = SQLAlchemy(application)
application.secret_key = "Superduperdupersecretkey"

application.config['secret_json_file'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client_secrets.json")

from controllers.homepage import homepage
from controllers.file_upload import fileupload
from controllers.metadata import metadata
from controllers.show_note import shownote
from controllers.oauth import oauth
from controllers.user import user

application.register_blueprint(homepage)
application.register_blueprint(fileupload)
application.register_blueprint(metadata)
application.register_blueprint(shownote)
application.register_blueprint(oauth)
application.register_blueprint(user)
