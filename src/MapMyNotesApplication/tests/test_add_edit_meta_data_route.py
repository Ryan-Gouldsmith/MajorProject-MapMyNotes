from MapMyNotesApplication import application, database
import pytest
import os
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from datetime import datetime
from flask import Flask
from flask.ext.testing import TestCase

class TestAddEditMetaDataRoute(TestCase):

    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")
        file_list = 'tests/test.png'.split("/")

        test_image_2 = "tests/test.png".split("/")

        self.image = file_list[1]
        self.second_image = test_image_2[1]
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_add_meta_data_route_returns_302(self):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        resource = self.client.post('/metadata/add/' + self.image,       content_type='multipart/form-data',
            data=post_data, follow_redirects=False)


        assert resource.status_code == 302

    def test_add_meta_data_route_get_request_not_allowed(self):
        resource = self.client.get('/metadata/add/' + self.image)
        assert resource.status_code == 405

    def test_add_module_code_via_post_request_successfully(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        assert len(Module_Code.query.all()) == 1

    def test_it_saves_a_note_object_once_the_meta_data_added(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        note = Note.query.first()
        assert note.image_path == "test.png"
        assert note.meta_data.module_code.module_code == "CS31310"
        assert note.meta_data.lecturer == "Mr Foo"
        assert note.meta_data.location == "C11 Hugh Owen"

    def test_once_a_note_is_saved_it_redirects_to_show_note(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        url_redirect = resource.headers.get("Location")
        url_path = url_redirect.split("http://localhost")

        expected_url = "/show_note/1"
        # checks the last part after the localhost.
        assert url_path[1] == expected_url

    def test_using_the_same_module_code_as_before_if_one_exists(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        second_resource = self.client.post("/metadata/add/" + self.second_image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)


        notes = Note.query.all()

        note_one = notes[0]

        note_two = notes[1]

        expected_module_code_id = note_one.meta_data.module_code.id

        assert expected_module_code_id == note_two.meta_data.module_code.id

    def test_using_the_different_module_code_should_save_new_code(self):
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        post_data_second = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        second_resource = self.client.post("/metadata/add/" + self.second_image,
                content_type='multipart/form-data',
                data=post_data_second, follow_redirects=False)

        notes = Note.query.all()

        note_one = notes[0]

        note_two = notes[1]

        actual = note_one.meta_data.module_code.id

        expected = note_two.meta_data.module_code.id

        assert actual != expected

    def test_get_edit_note_information_returns_200_success(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "A Title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        resource = self.client.get("/metadata/edit/" + str(note.id), follow_redirects=False)

        assert resource.status_code == 200

    def test_post_to_edit_note_different_data_created_new_meta_data(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        meta_data_change = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note.id), content_type='multipart/form-data',
        data=meta_data_change, follow_redirects=False)


        note_meta_data = Note_Meta_Data.query.all()
        assert len(note_meta_data) is 2

    def test_post_to_edit_note_changes_the_foreign_key_association(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note.id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)
        assert note_found.note_meta_data_id is 2

    def test_post_with_already_existing_meta_data_should_return_instance(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id


        module_code_two = Module_Code('CS361010')
        database.session.add(module_code_two)
        database.session.commit()
        module_code_id = module_code_two.id

        date = datetime.strptime("24 January 2016 16:00", "%d %B %Y %H:%M")

        changed_meta_data= Note_Meta_Data("Changed Text", module_code_id, 'Test room', date, "Another note title")
        changed_meta_data.save()
        changed_meta_data_id = changed_meta_data.id

        meta_data_change = {"module_code_data":"CS361010", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)

        assert note_found.meta_data.id == changed_meta_data_id

    def test_posting_exisiting_module_code_new_meta_data_new_instance(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Another note title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"CS31310", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)

        assert note_found.meta_data.id is 2

    def test_posting_redirects_back_to_show_note(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"CS31310", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        assert response.status_code == 302
        location = response.headers.get("Location").split("http://localhost/")
        assert location[1] == "show_note/1"
