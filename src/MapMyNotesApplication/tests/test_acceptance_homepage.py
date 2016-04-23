import os

import mock
from flask.ext.testing import LiveServerTestCase
from googleapiclient.http import HttpMock
from selenium import webdriver

from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User


class TestAcceptanceHomepage(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'Secret key'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__), "mock-data/authorised_credentials.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")

        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)

        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = OauthService()
        file_path = app.config['secret_json_file']
        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        self.credentials_oauth = oauth_service.exchange_code(flow, "123code", http=http_mock)
        cred_obj = oauth_service.create_credentials_from_json(self.credentials_oauth.to_json())
        auth = HttpMock(self.authorised_credentials, {'status': 200})
        self.oauth_return = oauth_service.authorise(auth, self.credentials_oauth.to_json())

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
        self.patch = mock.patch.object(SessionHelper, "check_if_session_contains_credentials")
        self.cred_mock = self.patch.start()
        self.cred_mock.return_value = True

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials_oauth.to_json()

        self.user_patch = mock.patch.object(SessionHelper, 'return_user_id')
        self.user_mock = self.user_patch.start()
        self.user_mock.return_value = 1

        self.oauth_patch = mock.patch.object(OauthService, "authorise")
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.oauth_return

        self.google_patch = mock.patch.object(GoogleCalendarService, "execute_request")
        self.google_mock = self.google_patch.start()
        self.google_mock.return_value = self.google_response

        self.credentials_patch = mock.patch.object(OauthService, 'get_credentials')
        self.credentials_mock = self.credentials_patch.start()
        self.credentials_mock.return_value = oauth_service.credentials



        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640)
        self.create_app()

    def tearDown(self):
        mock.patch.stopall()

    def stop(self):
        mock.patch.stopall()

    def test_should_display_the_correct_events_in_calendar(self):
        self.driver.get(self.get_server_url() + "/")
        events = self.driver.find_element_by_class_name("events")
        event = self.driver.find_element_by_class_name("event")
        summary = self.driver.find_element_by_class_name("summary")
        link = self.driver.find_element_by_class_name("link").get_attribute("href")

        assert events.is_displayed() is True
        assert event.is_displayed() is True
        assert summary.text == "Test Example"
        assert link == "https://www.google.com/calendar/event?testtest"

    def test_signing_in_does_not_show_the_sign_in_button(self):
        self.driver.get(self.get_server_url() + "/")
        welcome_div = self.driver.find_element_by_class_name("welcome")
        authorise = self.driver.find_elements_by_class_name("authorise")

        assert len(authorise) is 0
        assert welcome_div.is_displayed() is True

    def test_once_authorised_it_displays_users_email_address(self):
        self.driver.get(self.get_server_url() + "/")
        test_email = self.driver.find_element_by_class_name('welcome')
        assert test_email.text == "Welcome, test@gmail.com"