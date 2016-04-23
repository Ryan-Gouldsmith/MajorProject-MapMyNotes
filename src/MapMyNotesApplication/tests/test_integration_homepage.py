import os

import mock
from flask.ext.testing import TestCase
from googleapiclient.http import HttpMock

from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.user import User


class TestIntegrationHomePage(TestCase):
    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__), "mock-data/authorised_credentials.json")
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        return app

    def setUp(self):
        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)

        database.session.close()
        database.drop_all()
        database.create_all()

        user = User("test@gmail.com")
        database.session.add(user)

        database.session.commit()
        self.google_response = {"items": [
            {

                "kind": "calendar#event",
                "etag": "\"1234567891012345\"",
                "id": "ideventcalendaritem1",
                "status": "confirmed",
                "htmlLink": "https://www.google.com/calendar/event?testtest",
                "created": "2014-09-10T14:53:25.000Z",
                "updated": "2014-09-10T14:54:12.748Z",
                "summary": "Test Example",
                "creator": {
                    "email": "test@gmail.com",
                    "displayName": "Tester",
                    "self": 'true'
                },
                "organizer": {
                    "email": "test@gmail.com",
                    "displayName": "Test",
                    "self": 'true'
                },
                "start": {
                    "dateTime": "2016-12-01T01:00:00+01:00"
                },
                "end": {
                    "dateTime": "2016-12-01T02:30:00+01:00"
                },
                "transparency": "transparent",
                "visibility": "private",
                "iCalUID": "123456789@google.com",
                "sequence": 0,
                "guestsCanInviteOthers": 'false',
                "guestsCanSeeOtherGuests": 'false',
                "reminders": {
                    "useDefault": 'true'
                }
            }
        ]
        }

        # http://flask.pocoo.org/docs/0.10/testing/
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = OauthService()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
                                                      http=http_mock)

            oauth_service.create_credentials_from_json(credentials.to_json())

            self.auth_mock = HttpMock(self.authorised_credentials, {'status': 200})
            self.authorise = oauth_service.authorise(self.auth_mock, credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        self.credentials_patch = mock.patch.object(OauthService, 'get_credentials')
        self.credentials_mock = self.credentials_patch.start()
        self.credentials_mock.return_value = oauth_service.credentials

        self.oauth_patch = mock.patch.object(OauthService, 'authorise')
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.authorise

        self.google_request_patch = mock.patch.object(GoogleCalendarService, 'execute_request')
        self.google_request_mock = self.google_request_patch.start()
        self.google_request_mock.return_value = self.google_response

        self.create_app()

    def tearDown(self):
        mock.patch.stopall()

    def test_home_route(self):
        resource = self.client.get("/")

        assert resource.status_code == 200

    def test_displays_logout_link_if_logged_in(self):
        response = self.client.get("/")

        assert "logout" in response.data
        assert "/logout" in response.data

    def test_if_not_logged_in_it_doesnt_display_logout(self):
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.get("/")

        assert "logout" not in response.data

    def test_sign_in_displays_if_not_authorised(self):
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.get("/")

        assert "authorise" in response.data

    def test_credentials_not_in_session_return_blank_homepage(self):
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.get("/")

        assert "events" not in response.data
