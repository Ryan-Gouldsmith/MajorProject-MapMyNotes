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
