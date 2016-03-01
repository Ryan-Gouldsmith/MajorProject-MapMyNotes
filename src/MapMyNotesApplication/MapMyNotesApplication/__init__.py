from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mapmynotes'
database = SQLAlchemy(application)

from controllers.homepage import homepage
from controllers.file_upload import fileupload

application.register_blueprint(homepage)
application.register_blueprint(fileupload)
