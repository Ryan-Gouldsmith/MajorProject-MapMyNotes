class SessionHelper(object):

    def check_if_session_contains_credentials(self, session):
        return 'credentials' in session

    def return_session_credentials(self, session):
        return session['credentials']
