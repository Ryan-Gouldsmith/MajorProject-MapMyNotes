import os
from datetime import datetime

import mock
from flask import Flask
from flask.ext.testing import TestCase
from googleapiclient.http import HttpMock

from MapMyNotesApplication import database, application
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.google_services_helper import GoogleServicesHelper
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper


class TestGoogleServicesHelper(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        """
         http://blog.toast38coza.me/adding-a-database-to-a-flask-app/
         Used to help with the test database, could move this to a config file.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['SECRET_KEY'] = "secret"
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__), "mock-data/authorised_credentials.json")
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        self.events = {"items": [
            {

                "kind": "calendar#event",
                "etag": "\"1234567891012345\"",
                "id": "ideventcalendaritem1",
                "status": "confirmed",
                "htmlLink": "https://www.google.com/calendar/event?testtest",
                "created": "2014-09-10T14:53:25.000Z",
                "updated": "2014-09-10T14:54:12.748Z",
                "summary": "CS31310",
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
                    "dateTime": "2016-12-01T01:00:00"
                },
                "end": {
                    "dateTime": "2016-12-01T02:30:00"
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

        self.expected_event = {
            "kind": "calendar#event",
            "etag": "\"1234567891012345\"",
            "id": "ideventcalendaritem1",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?testtest",
            "created": "2014-09-10T14:53:25.000Z",
            "updated": "2014-09-10T14:54:12.748Z",
            "summary": "CS31310",
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
                "dateTime": "2016-12-01T01:00:00"
            },
            "end": {
                "dateTime": "2016-12-01T02:30:00"
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


        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            self.oauth_service = OauthService()
            file_path = application.config['secret_json_file']

            self.oauth_service.store_secret_file(file_path)
            flow = self.oauth_service.create_flow_from_clients_secret()

            self.credentials_auth = self.oauth_service.exchange_code(flow, "123code",
                                                                http=http_mock)
            self.oauth_service.create_credentials_from_json(self.credentials_auth.to_json())

            self.auth_mock = HttpMock(self.authorised_credentials, {'status': 200})
            self.authorise = self.oauth_service.authorise(self.auth_mock, self.credentials_auth.to_json())

            session['credentials'] = self.credentials_auth.to_json()
            session['user_id'] = 1
            self.session_helper = SessionHelper(session)

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials

        self.credentials_patch = mock.patch.object(OauthService, 'get_credentials')
        self.credentials_mock = self.credentials_patch.start()
        self.credentials_mock.return_value = self.oauth_service.credentials

        self.oauth_patch = mock.patch.object(OauthService, 'authorise')
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.authorise

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        self.calendar_response_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar_response.json")
        self.create_app()

    def tearDown(self):
        mock.patch.stopall()

    def test_get_event_containing_module_code_return_event_if_in_event(self):
        start_date = datetime.strptime("01 December 2016 01:00", "%d %B %Y %H:%M")
        contains = GoogleServicesHelper.get_event_containing_module_code("CS31310", self.events, start_date)

        assert contains == self.expected_event

    def test_get_event_containing_module_code_return_none_if_not_in_event(self):
        start_date = datetime.strptime("01 December 2016 01:00", "%d %B %Y %H:%M")
        contains = GoogleServicesHelper.get_event_containing_module_code("Not a module", self.events, start_date)

        assert contains is None

    def test_authorise_returns_credentials_and_http_auth_successfully(self):
        credentials, http_auth = GoogleServicesHelper.authorise(self.session_helper)

        assert credentials.to_json() == self.credentials_auth.to_json()
        assert type(http_auth) is HttpMock

    def test_get_events_based_on_date_time_returns_the_correct_google_response(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)
        http_mock = HttpMock(self.calendar_response_mock, {'status': '200'})
        start_date = datetime.strptime("01 December 2016 01:00", "%d %B %Y %H:%M")
        calendar_response = GoogleServicesHelper.get_events_based_on_date_time(start_date, calendar_service,service, http_mock)

        assert calendar_response['etag'] == "\"1234567891012345\""