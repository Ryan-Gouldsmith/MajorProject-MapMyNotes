from MapMyNotesApplication import application, database
import pytest
import os
from flask import request, Flask
from MapMyNotesApplication.models.note import Note
from flask.ext.testing import TestCase


class TestViewAllNotesRoute(TestCase):

    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_show_all_notes_returns_200_success_code(self):
        response = self.client.get("/view_notes")

        assert response.status_code is 200
