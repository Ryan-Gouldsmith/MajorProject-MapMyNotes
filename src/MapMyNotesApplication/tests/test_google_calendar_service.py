import pytest
from MapMyNotesApplication import application
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from oauth2client import client
from googleapiclient.http import HttpMock
from googleapiclient import discovery
import os
import json
from datetime import datetime
from flask.ext.testing import TestCase
from flask import Flask
"""
    Help with mocking idea from the source code of the test client - in the tests they perform mocking. Looking at the code for the actual client I'd be using helped to work out how to go about testing oAuth stuff. https://github.com/google/oauth2client/blob/master/tests/test_client.py

    All Mock data is generated from https://developers.google.com/google-apps/calendar/v3/reference/events/list#examples using the authors oAuthAPI then modified.
"""
class TestCalendarService(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        self.calendar_response_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar_response.json")
        self.calendar_week_response_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar_week_response.json")
        return app

    def test_building_the_discovery_in_calendar_service(self):
        calendar_service = Google_Calendar_Service()
        # Discovery mock json was the response from their test disvoery api. TODO Cite this properly and get the appropriate data needed.
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)

        assert type(service) is discovery.Resource
        assert service is not None

    def test_create_request_for_calendar(self):
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)

        request = calendar_service.get_list_of_events(service)

        expected_uri = "https://www.googleapis.com/calendar/v3/calendars/primary/events?alt=json"
        assert expected_uri in request.uri

    def test_executing_the_request_to_return_events_from_calendar(self):
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)
        request = calendar_service.get_list_of_events(service)

        http_mock = HttpMock(self.calendar_response_mock, {'status': '200'})

        requested_events = calendar_service.execute_request(request, http_mock)


        assert "items" in requested_events

        assert "guestsCanInviteOthers" in requested_events["items"][0]

    def test_getting_the_events_in_the_last_week(self):
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)
        date_start = datetime.strptime("01/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end =  datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        request = calendar_service.get_list_of_events(service, start=date_start, end=date_end)

        http_mock = HttpMock(self.calendar_week_response_mock, {'status': '200'})

        requested_events = calendar_service.execute_request(request, http_mock)

        returned_start = requested_events["items"][0]["start"]["dateTime"]

        returned_end = requested_events["items"][0]["end"]["dateTime"]

        assert 'items' in requested_events
        assert returned_start == '2016-12-01T01:00:00+01:00'

        assert returned_end == '2016-12-01T02:30:00+01:00'

    def test_getting_event_date_the_wrong_way_around_returns_false(self):
        calendar_service = Google_Calendar_Service()
        date_start = datetime.strptime("01/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end =  datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        response = calendar_service.check_dates_are_correct(start=date_start, end=date_end)

        assert response is True

    def test_getting_date_on_request_returns_none(self):
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)

        date_start = datetime.strptime("12/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        date_end =  datetime.strptime("08/12/2016 00:00:00", "%d/%m/%Y %H:%M:%S")

        request = calendar_service.get_list_of_events(service, start=date_start, end=date_end)

        assert request is None
