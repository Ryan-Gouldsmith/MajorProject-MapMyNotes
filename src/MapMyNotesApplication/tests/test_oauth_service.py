import pytest
from MapMyNotesApplication import application
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from oauth2client import client
from googleapiclient.http import HttpMock
import os
import json



class TestOAuthService(object):

    def setup(self):
        application.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        self.app = application.test_client()
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")

    def test_client_secret_file_exists(self):
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']
        assert oauth_service.client_secret_file_exists(file_path) is True

    def test_storing_the_client_note(self):
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']
        oauth_service.store_secret_file(file_path)
        assert "mock-data/client_secret.json" in oauth_service.client_secret_file

    def test_creation_of_flow_from_client_secrets_does_not_raise_an_error(self):
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']
        oauth_service.store_secret_file(file_path)
        assert oauth_service.create_flow_from_clients_secret() is not client.clientsecrets.InvalidClientSecretsError

    def test_creation_of_flow_returns_a_flow_object(self):
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']
        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()

        assert type(flow) is client.OAuth2WebServerFlow

    def test_returning_the_correct_authorisation_url(self):
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']
        oauth_service.store_secret_file(file_path)

        flow = oauth_service.create_flow_from_clients_secret()

        expected_url_encoded_response = "localhost%3A5000%2Foauthconfirm"

        assert expected_url_encoded_response in oauth_service.get_authorisation_url(flow)

    def test_exchanging_authorisation_codes_in_step_2(self):
        # Help with mocking idea from the source code of the test client. https://github.com/google/oauth2client/blob/master/tests/test_client.py
        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        credentials = oauth_service.exchange_code(flow, "123code",
        http=http_mock)

        assert 'foo' in credentials.token_response["access_token"]
        assert 10 is credentials.token_response["expires_in"]
        assert 'refresh' in credentials.token_response["refresh_token"]

    
