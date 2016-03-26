from MapMyNotesApplication import application, database
import pytest
import os
from flask import request
from datetime import datetime

class TestSearchRoute(object):

    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_search_route_with_code_returns_200_status_code(self):
        response = self.app.get("/search/CS31310")

        assert response.status_code == 200

    def test_search_route__with_code_can_not_permit_post_requests(self):
        response = self.app.post("/search/CS31310")
        assert response.status_code == 405

    def test_search_route_returns_200_status_code(self):
        response = self.app.get('/search')
        assert response.status_code == 200

    def test_search_with_post_request_returns_405(self):
        response = self.app.post("/search")
        assert response.status_code == 405
