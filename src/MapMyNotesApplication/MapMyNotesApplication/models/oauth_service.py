import os

from oauth2client import client

"""
    A Guide on how to create the OAuth2 exchange from Google:
    https://developers.google.com/api-client-library/python/guide/aaa_oauth.

    Modified to fit into a nicer design. There is only one way to do it with the Google OAuth however.
"""


class OauthService(object):
    def __init__(self):
        """
        Creates an instance of the OAuth Service object
        """
        self.client_secret_file = None
        self.credentials = None

    def client_secret_file_exists(self, file_path):
        """
        Checks to see if the client secret file does exist
        Parameters
        ----------
        file_path: The path to the file

        Returns
        -------
        True if it exists
        False if it does not exist
        """
        return os.path.isfile(file_path)

    def store_secret_file(self, file_path):
        """
        Parameters
        ----------
        file_path: Sets the file path to the current instance's attribute.
        """
        self.client_secret_file = file_path

    def create_flow_from_clients_secret(self):
        """
        Create the flow object from the client secrets file.
        Returns
        -------
        A Flow object from the client secret file with specific redirects back to the certain pages
        """
        return client.flow_from_clientsecrets(
            self.client_secret_file,
            scope=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email'],
            redirect_uri="http://localhost:5000/oauthsubmit"
        )

    def get_authorisation_url(self, flow_object):
        """
        Get the authorisation url with the code key
        Parameters
        ----------
        flow_object: The Flow object from the secret file

        Returns
        -------
        String representation of the authorised URL
        """
        return flow_object.step1_get_authorize_url()

    def exchange_code(self, flow_object, code, http=None):
        """
        Initial step of OAuth where there is the exchanging of the code for an access token.
        Parameters
        ----------
        flow_object: Flow object from secret file
        code: The code returned from the authorised url
        http: Httplib2 object to make the connection to the servide

        Returns
        -------
        A JSON response where the service has exchanged the token and returned an Access token
        """
        return flow_object.step2_exchange(code, http=http)

    def create_credentials_from_json(self, json_credentials):
        """
        Creates the JSON response into an object which will be stored in the session
        Parameters
        ----------
        json_credentials: The JSON response from exchanging the code.s

        """
        self.credentials = client.OAuth2Credentials.from_json(json_credentials)

    def authorise(self, http, json_credentials):
        """
        Creates the credentials from JSON and authorises the OAuth request to the service
        Parameters
        ----------
        http: HttpLib2 - used to make the request to the object
        json_credentials: Json credentials from when the exchanging of the code happended.

        Returns
        -------
        New instance of the http attribute.
        """
        self.create_credentials_from_json(json_credentials)
        return self.credentials.authorize(http)

    def get_credentials(self):
        """
        Returns
        -------
        Current instance's credentials.
        """
        return self.credentials
