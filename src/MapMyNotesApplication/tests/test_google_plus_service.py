import os

from MapMyNotesApplication.models.google_plus_service import GooglePlusService
from flask import Flask
from flask.ext.testing import TestCase
from googleapiclient import discovery
from googleapiclient.http import HttpMock, HttpRequest

"""
https://developers.google.com/api-client-library/python/guide/mocks#example
"""


class TestGooglePlusService(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/plus-discovery.json")
        self.google_plus_mock_response = os.path.join(os.path.dirname(__file__), "mock-data/google_plus_response.json")
        return app

    def test_build_the_google_plus_service_return_discovery_resource(self):
        google_plus_service = GooglePlusService()

        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = google_plus_service.build(http_mock)

        assert type(service) is discovery.Resource

    def test_request_to_get_user_logged_in(self):
        google_plus_service = GooglePlusService()

        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = google_plus_service.build(http_mock)

        request = google_plus_service.get_request_user_authorised(service)

        expected_uri = "https://www.googleapis.com/plus/v1/people/me?alt=json"

        assert type(request) is HttpRequest
        assert request.uri == expected_uri

    def test_executing_request_object_to_get_user_information(self):
        google_plus_service = GooglePlusService()

        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = google_plus_service.build(http_mock)

        request = google_plus_service.get_request_user_authorised(service)

        http_mock = HttpMock(self.google_plus_mock_response, {'status': '200'})

        returned_values = google_plus_service.execute_request(request, http_mock)

        expected = {'circledByCount': 100, 'emails': [{'type': 'account', 'value': 'test@gmail.com'}],
                    'objectType': 'person', 'occupation': 'A Test Occupation', 'tagline': 'Some Dummy data taglone',
                    'verified': 'False'}

        assert expected == returned_values

    def test_parsing_response_and_returning_the_email_address(self):
        google_plus_service = GooglePlusService()

        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = google_plus_service.build(http_mock)

        request = google_plus_service.get_request_user_authorised(service)

        http_mock = HttpMock(self.google_plus_mock_response, {'status': '200'})

        returned_values = google_plus_service.execute_request(request, http_mock)

        email_address = google_plus_service.parse_response_for_email(returned_values)

        assert email_address == 'test@gmail.com'
