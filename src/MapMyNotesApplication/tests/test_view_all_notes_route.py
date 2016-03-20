from MapMyNotesApplication import application, database
import pytest
import os
from flask import request
from MapMyNotesApplication.models.note import Note

class TestViewAllNotesRoute(object):

    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_show_all_notes_returns_200_success_code(self):
        response = self.app.get("/view_notes")

        assert response.status_code is 200
