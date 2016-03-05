from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data


class TestNote(object):
    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_saving_a_note(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen')
        note_meta_data.save()

        note = Note('uploads/', note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        assert note.id == 1

    def test_return_only_one_from_database(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen")
        note_meta_data.save()

        note = Note('uploaddirectory/foo.jpg',note_meta_data.id)
        database.session.add(note)
        database.session.commit()
        assert len(Note.query.all()) == 1

    def test_only_returns_a_note(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen")
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

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen")
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

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, "C11 Hugh Owen")
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

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen')
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

        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        assert note.meta_data.location == 'C11 Hugh Owen'
