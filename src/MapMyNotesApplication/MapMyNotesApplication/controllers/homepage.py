from flask import Blueprint, render_template, request, redirect, url_for, session
#from oauth2client import client
#import httplib2
#from apiclient import discovery


import json
import os
homepage = Blueprint('homepage', __name__)


@homepage.route("/")
def home_page_route():
    """
    print session
    if 'credentials' not in session:
        return redirect(url_for('homepage.oauthconfirm'))

    credentials = client.OAuth2Credentials.from_json(session['credentials'])

    http_auth = credentials.authorize(httplib2.Http())

    calendar_service = discovery.build('calendar', 'v3', http_auth)

    print calendar_service.events().list(calendarId='primary').execute()
"""




    return render_template('/homepage/index.html')
"""
@homepage.route("/oauthconfirm")
def oauthconfirm():
    client_secret_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'client_secrets.json')

    flow = client.flow_from_clientsecrets(
    client_secret_file,
    scope='https://www.googleapis.com/auth/calendar.readonly',
    redirect_uri="http://localhost:5000/oauthconfirm"
    )
    print request.args
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        #print credentials
        session['credentials'] = credentials.to_json()
        return redirect(url_for('homepage.home_page_route'))
    return render_template('/file_upload/index.html')
"""
