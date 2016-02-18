from flask import Flask

from controllers.homepage import homepage


application = Flask(__name__)
application.register_blueprint(homepage)
