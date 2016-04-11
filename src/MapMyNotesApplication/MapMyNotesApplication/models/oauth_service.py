import os

from oauth2client import client


class OauthService(object):
    def __init__(self):
        self.client_secret_file = None
        self.credentials = None

    def client_secret_file_exists(self, file_path):
        return os.path.isfile(file_path)

    def store_secret_file(self, file_path):
        self.client_secret_file = file_path

    def create_flow_from_clients_secret(self):
        return client.flow_from_clientsecrets(
            self.client_secret_file,
            scope=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email'],
            redirect_uri="http://localhost:5000/oauthsubmit"
        )

    def get_authorisation_url(self, flow_object):
        return flow_object.step1_get_authorize_url()

    def exchange_code(self, flow_object, code, http=None):
        return flow_object.step2_exchange(code, http=http)

    def create_credentials_from_json(self, json_credentials):
        self.credentials = client.OAuth2Credentials.from_json(json_credentials)

    def authorise(self, http, json_credentials):
        self.create_credentials_from_json(json_credentials)
        return self.credentials.authorize(http)

    def get_credentials(self):
        return self.credentials
