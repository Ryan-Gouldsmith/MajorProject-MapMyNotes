from MapMyNotesApplication import application, database
import pytest
import os
from flask import request
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from datetime import datetime

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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", "location_data" : "C11 Hugh Owen", "date_data": "12th February 2015 14:00", "title_data": "A Title"}
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        resource = self.app.post('/metadata/add/' + self.image,       content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        response = self.app.get('/show_note/1')
        assert response.status_code == 200

    def test_deleting_a_note_returns_status_code_200(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Title")
        note_meta_data.save()

        note = Note('uploads/', note_meta_data.id)
        note.save()

        resource = self.app.post('/delete_note/'+str(note.id))

        assert resource.status_code == 302

    def test_deleting_a_note_deletes_a_note_from_database(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Title")
        note_meta_data.save()

        note = Note('uploads/', note_meta_data.id)
        note.save()

        resource = self.app.post('/delete_note/'+str(note.id))

        notes = Note.query.all()

        assert len(notes) is 0
