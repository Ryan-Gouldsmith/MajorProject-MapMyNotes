from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.user import User
from datetime import datetime
from flask.ext.testing import TestCase
from flask import Flask


class TestOAuthRoute(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()
        self.module_code_id = module_code.id
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "title")
        note_meta_data.save()
        self.meta_data_id = note_meta_data.id

    def test_saving_a_note(self):
        note = Note('uploads/', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()
        assert note.id == 1

    def test_return_only_one_from_database(self):
        note = Note('uploaddirectory/foo.jpg', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()
        assert len(Note.query.all()) == 1

    def test_only_returns_a_note(self):
        note = Note('uploaddirectory/foo.jpg', self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()
        assert type(Note.query.first()) is Note

    def test_it_returns_the_correct_file_path(self):
        file_path = "upload/test.png"


        note = Note(file_path, self.meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()
        returned = Note.query.first()
        assert returned.image_path ==  file_path

    def test_the_save_function_in_a_note(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()
        returned = Note.query.first()
        assert returned.image_path == file_path
        assert len(Note.query.all()) == 1

    def test_getting_the_module_code_from_a_note(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        assert note.image_path == file_path
        assert note.meta_data.lecturer == "Mr Foo"

        assert note.meta_data.module_code.module_code == "CS31310"

    def test_getting_the_location_from_a_note(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        assert note.meta_data.location == 'C11 Hugh Owen'

    def test_deleting_a_note(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        note_2 = Note(file_path, self.meta_data_id, self.user_id)
        note_2.save()

        assert note.id == 1
        assert note_2.id == 2

        assert len(Note.query.all()) is 2

        note_2.delete()

        assert len(Note.query.all()) is 1

    def test_updating_meta_data_foreign_key_successfully(self):
        file_path = "upload/test.png"

        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data_new = Note_Meta_Data("Test", self.module_code_id, 'Testy', date, 'Title Other')
        note_meta_data_new.save()

        note.update_meta_data_id(note_meta_data_new.id)

        assert note.note_meta_data_id == 2
        assert note.meta_data.lecturer == "Test"

    def test_find_note_by_module_code(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        notes = Note.find_note_by_module_code("CS31310", self.user_id)

        assert len(notes) is 1
        assert notes[0].meta_data.lecturer == "Mr Foo"
        assert notes[0].user_id == self.user_id

    def test_finding_a_note_by_module_code_when_it_doesnt_exist(self):
        file_path = "upload/test.png"

        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()

        notes = Note.find_note_by_module_code("SE31520", self.user_id)

        assert len(notes) is 0

    def test_add_a_calendar_url_to_an_existing_object_successfully(self):
        file_path = "upload/test.png"

        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()
        note_id = note.id

        note.update_calendar_url("http://localhost/test")

        note = Note.query.get(note_id)

        assert note.calendar_url == "http://localhost/test"

    def test_saving_a_note_returns_the_correct_user_id(self):
        file_path = "upload/test.png"
        note = Note(file_path, self.meta_data_id, self.user_id)
        note.save()
        assert note.user_id is 1
