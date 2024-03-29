import os
from datetime import datetime

from flask import Flask
from flask.ext.testing import TestCase
from googleapiclient import discovery
from googleapiclient.http import HttpMock

from MapMyNotesApplication import database
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.user import User

"""
    Help with mocking idea from the source code of the test client - in the tests they perform mocking.
    Looking at the code for the actual client I'd be using helped to work out how to go about testing oAuth stuff.
    https://github.com/google/oauth2client/blob/master/tests/test_client.py

    All Mock data is generated from
    https://developers.google.com/google-apps/calendar/v3/reference/events/list#examples
     using the authors oAuthAPI then modified.

    Patch Method was used to be like a RESTful service instead of update:
    This resource told me what was returned so I could test that.
    https://developers.google.com/apis-explorer/#p/calendar/v3/calendar.events.patch
"""


class TestCalendarService(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['root_url'] = "http://localhost:5000"

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        self.calendar_response_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar_response.json")
        self.calendar_week_response_mock = os.path.join(os.path.dirname(__file__),
                                                        "mock-data/calendar_week_response.json")
        self.calendar_event_patched = os.path.join(os.path.dirname(__file__),
                                                   "mock-data/calendar_updated_description.json")

        self.calendar_no_description_link = os.path.join(os.path.dirname(__file__),
                                                         "mock-data/no_description_field.json")

        self.reoccurring_events = os.path.join(os.path.dirname(__file__), "mock-data/reoccurring_events.json")
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

        module_code = ModuleCode('CS31310')
        database.session.add(module_code)
        database.session.commit()
        self.module_code_id = module_code.id

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = NoteMetaData("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "title")
        note_meta_data.save()
        self.meta_data_id = note_meta_data.id

        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id

    def test_building_the_discovery_in_calendar_service(self):
        calendar_service = GoogleCalendarService()
        # Discovery mock json was the response from their test disvoery api.
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)

        assert type(service) is discovery.Resource
        assert service is not None

    def test_create_request_for_calendar(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)

        request = calendar_service.get_list_of_events(service)

        expected_uri = "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeZone=Europe%2FLondon&alt=json"
        assert expected_uri in request.uri

    def test_executing_the_request_to_return_events_from_calendar(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)
        request = calendar_service.get_list_of_events(service)

        http_mock = HttpMock(self.calendar_response_mock, {'status': '200'})

        requested_events = calendar_service.execute_request(request, http_mock)

        assert "items" in requested_events

        assert "guestsCanInviteOthers" in requested_events["items"][0]

    def test_getting_the_events_in_the_last_week(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)
        date_start = datetime.strptime("01/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end = datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        request = calendar_service.get_list_of_events(service, start=date_start, end=date_end)

        http_mock = HttpMock(self.calendar_week_response_mock, {'status': '200'})

        requested_events = calendar_service.execute_request(request, http_mock)

        returned_start = requested_events["items"][0]["start"]["dateTime"]

        returned_end = requested_events["items"][0]["end"]["dateTime"]

        assert 'items' in requested_events
        assert returned_start == '2016-12-01T01:00:00+01:00'

        assert returned_end == '2016-12-01T02:30:00+01:00'

    def test_getting_event_date_the_wrong_way_around_returns_false(self):
        calendar_service = GoogleCalendarService()
        date_start = datetime.strptime("01/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end = datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        response = calendar_service.check_dates_are_correct(start=date_start, end=date_end)

        assert response is True

    def test_getting_date_on_request_returns_none(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)

        date_start = datetime.strptime("12/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end = datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        request = calendar_service.get_list_of_events(service, start=date_start, end=date_end)

        assert request is None

    def test_preparing_a_link_to_add_an_events_description(self):
        note = Note('uploads/', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()

        calendar_service = GoogleCalendarService()
        note_url = calendar_service.prepare_url_for_event(note)

        assert note_url == "http://localhost:5000/show_note/1"

    def test_adding_note_url_to_calendar_event(self):
        note = Note('uploads/', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()

        calendar_service = GoogleCalendarService()
        event = {
            "kind": "calendar#event",
            "etag": "\"12334455667\"",
            "id": "123456789",
            "status": "confirmed",
            "htmlLink": "https://test",
            "created": "2016-03-24T08:59:46.000Z",
            "updated": "2016-03-27T21:10:42.379Z",
            "summary": "Test To Show Hannah",
            "creator": {
                "email": "test@gmail.com",
                "displayName": "Test",
                "self": True
            },
            "organizer": {
                "email": "test@gmail.com",
                "displayName": "test",
                "self": True
            },
            "start": {
                "dateTime": "2016-03-24T07:30:00Z"
            },
            "end": {
                "dateTime": "2016-03-24T08:30:00Z"
            },
            "iCalUID": "test124@google.com",
            "sequence": 0,
            "reminders": {
                "useDefault": True
            }
        }

        note_url = calendar_service.prepare_url_for_event(note)
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)
        event_id = "ideventcalendaritem1"
        http_auth = HttpMock(self.calendar_event_patched, {'status': '200'})
        requested_event = calendar_service.add_note_url_to_description(note_url, event, service, http_auth)

        assert requested_event['description'] == '"http://localhost:5000/show_note/1"'

    def test_get_events_based_on_date_returns_correct_events(self):
        note = Note('uploads/', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()

        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})

        service = calendar_service.build(http_mock)
        date_start = datetime.strptime("10/09/2016 12:00:00", "%d/%m/%Y %H:%M:%S")

        date_end = datetime.strptime("10/09/2016 23:59:59", "%d/%m/%Y %H:%M:%S")

        request = calendar_service.get_list_of_events(service, start=date_start, end=date_end)

        http_mock = HttpMock(self.calendar_response_mock, {'status': '200'})
        requested_events = calendar_service.get_events_based_on_date(date_start, date_end, http_mock, service)

        assert '2014-09-10T19:00:00' in requested_events['items'][0]['start']['dateTime']

    def test_remove_note_url_from_description_removes_the_value_from_the_event(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)

        note = Note('uploads/', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()

        calendar_service = GoogleCalendarService()
        event = {
            "kind": "calendar#event",
            "etag": "\"12334455667\"",
            "id": "123456789",
            "status": "confirmed",
            "htmlLink": "https://test",
            "created": "2016-03-24T08:59:46.000Z",
            "updated": "2016-03-27T21:10:42.379Z",
            "summary": "Test To Show Hannah",
            "creator": {
                "email": "test@gmail.com",
                "displayName": "Test",
                "self": True
            },
            "description": "http://localhost:5000/show_note/1",
            "organizer": {
                "email": "test@gmail.com",
                "displayName": "test",
                "self": True
            },
            "start": {
                "dateTime": "2016-03-24T07:30:00Z"
            },
            "end": {
                "dateTime": "2016-03-24T08:30:00Z"
            },
            "iCalUID": "test124@google.com",
            "sequence": 0,
            "reminders": {
                "useDefault": True
            }
        }

        note_url = calendar_service.prepare_url_for_event(note)
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)
        http_auth = HttpMock(self.calendar_no_description_link, {'status': '200'})

        responded_event = calendar_service.remove_note_url_from_description(note_url, event, service, http_auth)

        assert '"http://localhost:5000/show_note/1"' not in responded_event['description']

    def test_get_recurring_event_list_returns_the_instance_list_of_events(self):
        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)

        date_start = datetime.strptime("12/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end = datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")
        event_id = "123456789"

        http_auth = HttpMock(self.reoccurring_events, {'status': '200'})
        responded_events = calendar_service.get_recurring_event_list(date_start, date_end, event_id, http_auth, service)

        assert 'recurringEventId' in responded_events['items'][0]
