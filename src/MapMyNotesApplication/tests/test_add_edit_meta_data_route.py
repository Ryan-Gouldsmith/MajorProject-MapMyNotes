from MapMyNotesApplication import application, database
import pytest
import os
from flask import request
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code




class TestAddEditMetaDataRoute(object):

    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()
        file_list = 'tests/test.png'.split("/")

        self.image = file_list[1]

    def test_add_meta_data_route_returns_302(self):
        post_data = {"module_code_data":"CS31310"}
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        resource = self.app.post('/metadata/add/' + self.image,       content_type='multipart/form-data',
            data={"module_code_data":"CS31310"}, follow_redirects=False)


        assert resource.status_code == 302

    def test_add_meta_data_route_get_request_not_allowed(self):
        resource = self.app.get('/metadata/add/' + self.image)
        assert resource.status_code == 405

    def test_add_module_code_via_post_request_successfully(self):
        post_data = {"module_code_data":"CS31310"}
        resource = self.app.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data={"module_code_data":"CS31310"}, follow_redirects=False)

        assert len(Module_Code.query.all()) == 1

    def test_it_saves_a_note_object_once_the_meta_data_added(self):
        post_data = {"module_code_data":"CS31310"}
        resource = self.app.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data={"module_code_data":"CS31310"}, follow_redirects=False)

        note = Note.query.first()
        assert note.image_path == "test.png"
        assert note.module_code.module_code == "CS31310"

    def test_once_a_note_is_saved_it_redirects_to_show_note(self):
        post_data = {"module_code_data":"CS31310"}
        resource = self.app.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data={"module_code_data":"CS31310"}, follow_redirects=False)

        url_redirect = resource.headers.get("Location")
        url_path = url_redirect.split("http://localhost")

        expected_url = "/show_note/1"
        # checks the last part after the localhost.
        assert url_path[1] == expected_url
