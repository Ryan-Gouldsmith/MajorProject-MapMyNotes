class SessionHelper(object):
    def __init__(self, session):
        """
        Initialises a session helper
        Parameters
        ----------
        session: The current session in the application
        """
        self.session = session

    def check_if_session_contains_credentials(self):
        """
        Returns
        -------
        True if the credentials are in the session
        False if they are not in the session
        """
        return 'credentials' in self.session

    def return_session_credentials(self):
        """
        Returns
        -------
        The JSON session credentials from the session
        """
        return self.session['credentials']

    def return_user_id(self):
        """
        Returns
        -------
        An Int representing the user's ID.
        """
        return self.session['user_id']

    def is_user_id_in_session(self):
        """
        Returns
        -------
        True if the user's id is in the session
        False if the user's id is not in the session
        """
        return 'user_id' in self.session

    def errors_in_session(self):
        """
        Returns
        -------
        True if there are errors in the session
        False if there are not errors in the session
        """
        return 'errors' in self.session

    def get_errors(self):
        """
        Returns
        -------
        A string of errors from the session
        """
        return self.session['errors']

    def delete_session_errors(self):
        """
        Deletes the errors from the session
        """
        del self.session['errors']

    def set_errors_in_session(self, errors):
        """
        Sets the erros in the session as a string
        Parameters
        ----------
        errors: String representation of the errors.
        """
        self.session['errors'] = errors

    def save_user_id_to_session(self, user_id):
        """
        Saves a user id to the session
        Parameters
        ----------
        user_id: Int representation of the user
        """
        self.session['user_id'] = user_id

    def delete_credentials_from_session(self):
        """
        Checks to see if the session contains the credentials and then attempts to remove them
        """
        if self.check_if_session_contains_credentials() is True:
            del self.session['credentials']

    def delete_user_from_session(self):
        """
        Checks to see if the user id is in the session if it is then it will delete the session
        """
        if self.is_user_id_in_session() is True:
            del self.session['user_id']

    def save_credentials_to_session(self, credentials):
        """
        Save the OAuth credentials to the session
        Parameters
        ----------
        credentials: JSON response from the credentials are saved to the session
        """
        self.session['credentials'] = credentials
