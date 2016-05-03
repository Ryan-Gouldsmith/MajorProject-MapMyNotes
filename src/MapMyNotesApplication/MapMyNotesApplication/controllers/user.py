from flask import Blueprint, url_for, redirect, session

from MapMyNotesApplication.models.google_plus_service import GooglePlusService
from MapMyNotesApplication.models.google_services_helper import GoogleServicesHelper
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User

user = Blueprint('user', __name__)


@user.route('/signin')
def signin():
    """
    Helps to connect with the OAuth service and  connect to the Google+ api to authorise and
    get the email address from a user and save it in the relation.
    """
    session_helper = SessionHelper(session)
    if session_helper.check_if_session_contains_credentials() is False:
        return redirect(url_for('oauth.oauthsubmit'))

    credentials, http_auth = GoogleServicesHelper.authorise(session_helper)
    google_plus_service = GooglePlusService()
    google_service = google_plus_service.build(http_auth)
    google_request = google_plus_service.get_request_user_authorised(google_service)
    google_plus_response = google_plus_service.execute_request(google_request, http_auth)
    email_address = google_plus_service.parse_response_for_email(google_plus_response)

    user = User.find_user_by_email_address(email_address)

    if user is None:
        user = User(email_address)
        user.save()

    session_helper.save_user_id_to_session(user.id)

    return redirect(url_for('homepage.home_page_route'))
