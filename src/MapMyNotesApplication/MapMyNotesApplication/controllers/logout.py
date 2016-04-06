from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
from MapMyNotesApplication.models.session_helper import SessionHelper
logoutblueprint = Blueprint('logout', __name__)


@logoutblueprint.route("/logout", methods=["GET"])
def logout():
    # Remove credentials key from session
    session_helper = SessionHelper()
    session_helper.delete_credentials_from_session(session)
    session_helper.delete_user_from_session(session)
    # Remove the user id from session
    return redirect(url_for('homepage.home_page_route'))
