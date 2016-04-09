from MapMyNotesApplication.models.oauth_service import OauthService
from flask import Blueprint, request, url_for, redirect, current_app, session

oauth = Blueprint('oauth', __name__)

"""
 Modified from the tutorial and documentation on google for the api client.
 I wrote the information into a service object instead and added associated tests.
 https://developers.google.com/api-client-library/python/auth/web-app#example
"""


@oauth.route('/oauthsubmit', methods=["GET"])
def oauthsubmit():
    oauth_service = OauthService()
    client_secrets_file = current_app.config['secret_json_file']

    if oauth_service.client_secret_file_exists(client_secrets_file):
        oauth_service.store_secret_file(client_secrets_file)

        flow = oauth_service.create_flow_from_clients_secret()

        if 'code' not in request.args:
            authorisation_uri = oauth_service.get_authorisation_url(flow)
            return redirect(authorisation_uri)
        else:
            code = request.args.get('code')
            # DEFAULT HTTP
            credentials = oauth_service.exchange_code(flow, code)
            # TODO replace with session helper
            session['credentials'] = credentials.to_json()
            return redirect(url_for('user.signin'))
    else:
        return 'Error with the key, contact an admin'
