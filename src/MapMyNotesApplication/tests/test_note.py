from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
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

    def test_saving_a_note(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "title")
        note_meta_data.save()

        note = Note('uploads/', note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        assert note.id == 1

    def test_return_only_one_from_database(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen", date, "Title")
        note_meta_data.save()

        note = Note('uploaddirectory/foo.jpg',note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        assert len(Note.query.all()) == 1

    def test_only_returns_a_note(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen", date, "Title")
        note_meta_data.save()

        note = Note('uploaddirectory/foo.jpg',note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        assert type(Note.query.first()) is Note

    def test_it_returns_the_correct_file_path(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen", date, "Title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        returned = Note.query.first()
        assert returned.image_path ==  file_path

    def test_the_save_function_in_a_note(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen", date, "Title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        returned = Note.query.first()
        assert returned.image_path == file_path
        assert len(Note.query.all()) == 1

    def test_getting_the_module_code_from_a_note(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        assert note.image_path == file_path
        assert note.meta_data.lecturer == "Mr Foo"

        assert note.meta_data.module_code.module_code == "CS31310"

    def test_getting_the_location_from_a_note(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        assert note.meta_data.location == 'C11 Hugh Owen'

    def test_deleting_a_note(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        note_2 = Note(file_path,note_meta_data.id)
        note_2.save()

        assert note.id == 1
        assert note_2.id == 2

        assert len(Note.query.all()) is 2

        note_2.delete()

        assert len(Note.query.all()) is 1

    def test_updating_meta_data_foreign_key_successfully(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        note_meta_data_new = Note_Meta_Data("Test", module_code.id, 'Testy', date, 'Title Other')
        note_meta_data_new.save()

        note.update_meta_data_id(note_meta_data_new.id)

        assert note.note_meta_data_id == 2
        assert note.meta_data.lecturer == "Test"

    def test_find_note_by_module_code(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        notes = Note.find_note_by_module_code("CS31310")

        assert len(notes) is 1
        assert notes[0].meta_data.lecturer == "Mr Foo"

    def test_finding_a_note_by_module_code_when_it_doesnt_exist(self):
        file_path = "upload/test.png"

        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        notes = Note.find_note_by_module_code("SE31520")

        assert len(notes) is 0
