from MapMyNotesApplication.models.session_helper import SessionHelper
from flask import Blueprint, url_for, redirect, session

logoutblueprint = Blueprint('logout', __name__)

GET = 'GET'


@logoutblueprint.route("/logout", methods=[GET])
def logout():
    # Remove credentials key and user id from session
    session_helper = SessionHelper(session)
    session_helper.delete_credentials_from_session()
    session_helper.delete_user_from_session()
    return redirect(url_for('homepage.home_page_route'))
