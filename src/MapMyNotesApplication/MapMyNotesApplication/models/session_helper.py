class SessionHelper(object):

    def check_if_session_contains_credentials(self, session):
        return 'credentials' in session

    def return_session_credentials(self, session):
        return session['credentials']

    def return_user_id(self, session):
        return session['user_id']

    def is_user_id_in_session(self, session):
        return 'user_id' in session

    def errors_in_session(self, session):
        return 'errors' in session

    def get_errors(self, session):
        return session['errors']

    def delete_session_errors(self, session):
        del session['errors']

    def set_errors_in_session(self, session, errors):
        session['errors'] = errors

    def save_user_id_to_session(self, session, user_id):
        session['user_id'] = user_id
