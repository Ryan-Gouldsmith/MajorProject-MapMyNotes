import os

import mock
from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.google_plus_service import GooglePlusService
from MapMyNotesApplication.models.oauth_service import OauthService
from flask.ext.testing import TestCase
from googleapiclient.http import HttpMock

"""
Reference https://www.theodo.fr/blog/2015/07/functional-testing-in-an-environment-of-flask-micro-services/

Referenc
http://www.voidspace.org.uk/python/mock/patch.html
"""


class TestIntegrationUser(TestCase):
    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),
                                                   "mock-data/authorised_credentials.json")

        self.google_plus_mock_response = os.path.join(os.path.dirname(__file__), "mock-data/google_plus_response.json")
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/plus-discovery.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),
                                                   "mock-data/authorised_credentials.json")

        return app

    def setUp(self):
        google_service = GooglePlusService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = google_service.build(http_mock)

        database.session.close()
        database.drop_all()
        database.create_all()

    @mock.patch.object(OauthService, 'authorise')
    @mock.patch.object(GooglePlusService, 'execute_request')
    def test_user_route(self, http, google):
        # http://flask.pocoo.org/docs/0.10/testing/
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = OauthService()
            file_path = application.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
                                                      http=http_mock)
            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()

        auth = HttpMock(self.authorised_credentials, {'status': 200})
        oauth_return = OauthService.authorise(auth, credentials.to_json())
        OauthService.authorise.return_value = oauth_return

        GooglePlusService.execute_request.return_value = {'circledByCount': 100,
                                                    'emails': [{'type': 'account', 'value': 'test@gmail.com'}],
                                                    'objectType': 'person', 'occupation': 'A Test Occupation',
                                                    'tagline': 'Some Dummy data taglone', 'verified': 'False'}
        response = self.client.get("/signin")

        url_full = response.headers.get("Location")

        url_path = url_full.split("http://localhost")

        assert url_path[1] == "/"

        assert response.status_code == 302
