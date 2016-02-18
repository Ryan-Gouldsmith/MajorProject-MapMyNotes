from flask import Blueprint, render_template
homepage = Blueprint('homepage', __name__)


@homepage.route("/")
def home_page_route():
    return render_template('/homepage/index.html')
