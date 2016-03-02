from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
import tempfile

class TestNote(object):
    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_saving_a_note(self):
        note = Note('uploads/')
        database.session.add(note)
        database.session.commit()
        assert note.id == 1

    def test_return_only_one_from_database(self):
        note = Note('uploaddirectory/foo.jpg')
        database.session.add(note)
        database.session.commit()
        assert len(Note.query.all()) == 1

    def test_only_returns_a_note(self):
        note = Note('uploaddirectory/foo.jpg')
        database.session.add(note)
        database.session.commit()
        assert type(Note.query.first()) is Note

    def test_it_returns_the_correct_file_path(self):
        file_path = "upload/test.png"
        note = Note(file_path)
        database.session.add(note)
        database.session.commit()
        returned = Note.query.first()
        assert returned.image_path ==  file_path

    def test_the_save_function_in_a_note(self):
        file_path = "upload/test.png"
        note = Note(file_path)
        note.save()
        returned = Note.query.first()
        assert returned.image_path == file_path
        assert len(Note.query.all()) == 1
