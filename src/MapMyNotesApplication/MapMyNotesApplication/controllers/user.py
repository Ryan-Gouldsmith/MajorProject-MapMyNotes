from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
import httplib2
from MapMyNotesApplication.models.google_plus_service import Google_Plus_Service
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.user import User
from MapMyNotesApplication.models.session_helper import SessionHelper

user = Blueprint('user', __name__)

@user.route('/signin')
def signin():
    session_helper = SessionHelper()
    if session_helper.check_if_session_contains_credentials(session) is False:
        return redirect(url_for('oauth.oauthsubmit'))

    service = Oauth_Service()
    session_credentials = session_helper.return_session_credentials(session)
    credentials = service.create_credentials_from_json(session_credentials)

    http_auth = service.authorise(credentials, httplib2.Http())

    google_plus_service = Google_Plus_Service()

    google_service = google_plus_service.build(http_auth)

    google_request = google_plus_service.get_request_user_authorised(google_service)

    google_plus_response = google_plus_service.execute(google_request, http_auth)

    email_address = google_plus_service.parse_response_for_email(google_plus_response)

    user = User.find_user_by_email_address(email_address)
    if user is None:
        user = User(email_address)
        user.save()

    session_helper.save_user_id_to_session(session, user.id)

    return redirect(url_for('homepage.home_page_route'))
