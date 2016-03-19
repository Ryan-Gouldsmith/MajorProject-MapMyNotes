from flask import Blueprint, render_template, request, url_for, redirect, current_app, session

import httplib2


from MapMyNotesApplication.models.google_plus_service import Google_Plus_Service
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.user import User

user = Blueprint('user', __name__)

@user.route('/signin')
def signin():
    if 'credentials' not in session:
        return redirect(url_for('oauth.oauthsubmit'))

    service = Oauth_Service()
    session_credentials = session['credentials']
    credentials = service.create_credentials_from_json(session_credentials)

    http_auth = service.authorise(credentials, httplib2.Http())

    google_plus_service = Google_Plus_Service()

    google_service = google_plus_service.build(http_auth)

    google_request = google_plus_service.get_request_user_authorised(google_service)

    google_plus_response = google_plus_service.execute(google_request, http_auth)

    email_address = google_plus_service.parse_response_for_email(google_plus_response)

    user = User(email_address)
    user.save()

    return redirect(url_for('homepage.home_page_route'))
