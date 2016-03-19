from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask.ext.testing import LiveServerTestCase
import mock
from googleapiclient.http import HttpMock, HttpRequest
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from MapMyNotesApplication.controllers.homepage import cookie_in_session
import os
import pprint

class TestIntegrationHomepage(object):

    def setup(self):
        application.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")
        self.app = application.test_client()


    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_should_display_the_correct_events_in_calendar(self, authorise, request):
        with self.app.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = application.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)
            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        Oauth_Service.authorise.return_value = oauth_return


        Google_Calendar_Service.execute_request.return_value = {"items": [
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

        response = self.app.get("/")
        response_data = response.data.replace("\n", '')
        assert '<section class="events">' in response_data
        assert '<div class="event">' in response_data
        assert '<p class="summary">Test Example</p>' in response_data
        assert '<a href="https://www.google.com/calendar/event?testtest">View event</a>' in response_data
