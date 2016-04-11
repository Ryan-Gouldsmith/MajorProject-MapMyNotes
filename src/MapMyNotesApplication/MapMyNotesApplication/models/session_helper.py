class SessionHelper(object):
    def __init__(self, session):
        self.session = session

    def check_if_session_contains_credentials(self):
        return 'credentials' in self.session

    def return_session_credentials(self):
        return self.session['credentials']

    def return_user_id(self):
        return self.session['user_id']

    def is_user_id_in_session(self):
        return 'user_id' in self.session

    def errors_in_session(self):
        return 'errors' in self.session

    def get_errors(self):
        return self.session['errors']

    def delete_session_errors(self):
        del self.session['errors']

    def set_errors_in_session(self, errors):
        self.session['errors'] = errors

    def save_user_id_to_session(self, user_id):
        self.session['user_id'] = user_id

    def delete_credentials_from_session(self):
        if self.check_if_session_contains_credentials() is True:
            del self.session['credentials']

    def delete_user_from_session(self):
        if self.is_user_id_in_session() is True:
            del self.session['user_id']

    def save_credentials_to_session(self, credentials):
        self.session['credentials'] = credentials
