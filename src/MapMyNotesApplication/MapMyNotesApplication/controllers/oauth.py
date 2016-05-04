from flask import Blueprint, request, url_for, redirect, current_app, session

from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper

oauth = Blueprint('oauth', __name__)

"""
 Modified from the tutorial and documentation on google for the api client.
 I wrote the information into a service object instead and added associated tests.
 https://developers.google.com/api-client-library/python/auth/web-app#example
"""

GET = "GET"


@oauth.route('/oauthsubmit', methods=[GET])
def oauthsubmit():
    """
    Uses the Google API Client library to authenticate with Google.
    """
    oauth_service = OauthService()
    #get the client secret
    client_secrets_file = current_app.config['secret_json_file']
    session_helper = SessionHelper(session)
    #checks it exists
    if oauth_service.client_secret_file_exists(client_secrets_file):
        oauth_service.store_secret_file(client_secrets_file)
        #create a flow
        flow = oauth_service.create_flow_from_clients_secret()

        if 'code' not in request.args:
            # see if the code is in the url
            authorisation_uri = oauth_service.get_authorisation_url(flow)
            return redirect(authorisation_uri)
        else:
            #get the code from the url
            code = request.args.get('code')
            #exhange the code
            credentials = oauth_service.exchange_code(flow, code)
            session_helper.save_credentials_to_session(credentials.to_json())
            return redirect(url_for('user.signin'))
    else:
        return 'Error with the key, contact an admin'
