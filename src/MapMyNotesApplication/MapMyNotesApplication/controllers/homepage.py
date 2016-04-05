from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
import httplib2
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from MapMyNotesApplication.models.user import User
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.session_helper import SessionHelper
from datetime import datetime, timedelta
import json
import os
homepage = Blueprint('homepage', __name__)


@homepage.route("/")
def home_page_route():
    session_helper = SessionHelper()
    if session_helper.check_if_session_contains_credentials(session) is True:
        service = Oauth_Service()
        session_credentials = session_helper.return_session_credentials(session)
        credentials = service.create_credentials_from_json(session_credentials)
        http_auth = service.authorise(credentials, httplib2.Http())
        # https://developers.google.com/identity/protocols/OAuth2WebServer#example Reference for the access token expiration
        if credentials.access_token_expired is False:
            google_calendar_service = Google_Calendar_Service()
            google_service = google_calendar_service.build(http_auth)

        # Google requires it to be in  RFC 3339 format. http://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python Reference.
            end_date = datetime.utcnow().isoformat("T") + "Z"
            start_date = (datetime.utcnow() - timedelta(days=7)).isoformat("T") + "Z"
            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date,end=end_date)

            google_calendar_response =  google_calendar_service.execute_request(google_request, http_auth)

            events = google_calendar_response['items']

            email_address = User.query.get(session['user_id']).email_address

            return render_template('/homepage/index.html', events=events, email_address=email_address)

    return render_template('/homepage/index.html')
