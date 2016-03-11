import pytest
from MapMyNotesApplication import application
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from oauth2client import client
from googleapiclient.http import HttpMock
from googleapiclient import discovery
import os
import json
import pprint

"""
    Help with mocking idea from the source code of the test client - in the tests they perform mocking. Looking at the code for the actual client I'd be using helped to work out how to go about testing oAuth stuff. https://github.com/google/oauth2client/blob/master/tests/test_client.py
"""
class TestCalendarService(object):

    def setup(self):
        application.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        self.app = application.test_client()
        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")


    def test_building_the_discovery_in_calendar_service(self):
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})

        service = calendar_service.build(http_mock)

        assert type(service) is discovery.Resource
        assert service is not None
