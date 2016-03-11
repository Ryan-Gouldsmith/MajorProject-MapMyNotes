from flask import Blueprint, render_template, request, url_for, redirect, current_app

from MapMyNotesApplication.models.oauth_service import Oauth_Service

oauth = Blueprint('oauth', __name__)

@oauth.route('/oauthsubmit', methods=["POST"])
def oauthsubmit():
    oauth_service = Oauth_Service()
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
            session['credentials'] = credentials.to_json()
            return redirect(url_for('homepage.home_page_route'))
    else:
        return 'Error with the key, contact an admin'
