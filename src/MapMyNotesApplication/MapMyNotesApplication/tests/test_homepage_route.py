from MapMyNotesApplication.MapMyNotesApplication import application
import pytest
import os


class TestHomePageRoute(object):

    def setup(self):
        self.app = application.test_client()

    def test_home_route(self):
        resource = self.app.get("/")
        assert resource.status_code == 200
