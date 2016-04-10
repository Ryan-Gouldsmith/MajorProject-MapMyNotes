from flask import Blueprint, render_template, url_for, redirect, session

from MapMyNotesApplication.models.date_time_helper import DateTimeHelper
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.google_services_helper import GoogleServicesHelper
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User

homepage = Blueprint('homepage', __name__)


@homepage.route("/")
def home_page_route():
    session_helper = SessionHelper(session)
    if session_helper.check_if_session_contains_credentials():
        credentials, http_auth = GoogleServicesHelper.authorise(session_helper)
        """
        https://developers.google.com/identity/protocols/OAuth2WebServer#example
        Reference for the access token expiration
        """
        if not credentials.access_token_expired:
            google_calendar_service = GoogleCalendarService()
            google_service = google_calendar_service.build(http_auth)

            """Google requires it to be in  RFC 3339 format.
             http://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python Reference.
            """
            end_date, start_date = DateTimeHelper.get_last_7_days_of_dates()
            google_calendar_response = google_calendar_service.get_events_based_on_date(start_date, end_date, http_auth,
                                                                                        google_service)
            events = google_calendar_response['items']

            user_id = session_helper.return_user_id()
            email_address = User.query.get(user_id).email_address

            return render_template('/homepage/index.html', events=events, email_address=email_address)
        else:
            return redirect(url_for('logout.logout'))

    return render_template('/homepage/index.html')
