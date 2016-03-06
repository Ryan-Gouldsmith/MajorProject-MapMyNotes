from MapMyNotesApplication import application, database
import pytest
import os
from flask import request


class TestShowNoteRoute(object):

    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()
        file_list = 'tests/test.png'.split("/")

        self.image = file_list[1]

    def test_route_returns_status_code_200(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", "location_data" : "C11 Hugh Owen", "date_data": "12th February 2015 14:00"}
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        resource = self.app.post('/metadata/add/' + self.image,       content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        response = self.app.get('/show_note/1')
        assert response.status_code == 200
