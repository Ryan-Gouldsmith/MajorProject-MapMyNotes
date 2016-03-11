import os
from oauth2client import client

class Oauth_Service(object):

    #CLIENT_SECRET_FILE = 'client_secrets.json'
    client_secret_file = ""

    def client_secret_file_exists(self, file_path):
        return os.path.isfile(file_path)

    def store_secret_file(self, file_path):
        self.client_secret_file = file_path

    def create_flow_from_clients_secret(self):
        return client.flow_from_clientsecrets(
        self.client_secret_file,
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri="http://localhost:5000/oauthconfirm"
        )

    def get_authorisation_url(self, flow_object):
        return flow_object.step1_get_authorize_url()

    def exchange_code(self, flow_object, code, http=None):
        return flow_object.step2_exchange(code, http=http)
