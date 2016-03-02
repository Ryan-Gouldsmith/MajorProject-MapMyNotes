from flask import Flask

from controllers.homepage import homepage
from controllers.file_upload import fileupload


application = Flask(__name__)
application.register_blueprint(homepage)
application.register_blueprint(fileupload)
