from flask import session

class SessionHelper(object):

    def check_if_session_contains_credentials(self):
        return 'credentials' in session

    def return_session_credentials(self):
        return session['credentials']
