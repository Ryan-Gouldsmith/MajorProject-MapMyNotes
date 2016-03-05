from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code

class TestNoteMetaData(object):
    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_saving_a_lecturers_name_should_return_correct_name(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        meta_data = Note_Meta_Data("Dr Test", module_code.id)
        database.session.add(meta_data)
        database.session.commit()

        database_meta_data = Note_Meta_Data.query.first()

        assert database_meta_data.lecturer == meta_data.lecturer

    def test_the_save_function_in_note_meta_data(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        meta_data = Note_Meta_Data("Dr Test", module_code.id)
        meta_data.save()

        database_meta_data = Note_Meta_Data.query.first()

        assert database_meta_data.lecturer == meta_data.lecturer

    def test_a_name_which_is_too_long_should_return_false(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        too_long_lecturers_name = "a" * 100
        meta_data = Note_Meta_Data(too_long_lecturers_name, module_code.id)
        result = meta_data.save()
        assert False is result

    def test_a_name_which_is_fine_for_length_should_return_true(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        lecturer_name = "Dr Mark Foobar"
        meta_data = Note_Meta_Data(lecturer_name, module_code.id)

        result = meta_data.save()

        assert True is result

    def test_it_saves_a_meta_data_note_and_returns_correct_id(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        meta_data = Note_Meta_Data("Dr Test", module_code.id)
        meta_data.save()

        expected_id = 1

        assert meta_data.id == expected_id

    def test_saves_a_module_code_as_part_of_a_foreign_key(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        meta_data = Note_Meta_Data("Dr Test", module_code.id)

        meta_data.save()

        assert meta_data.module_code.module_code == "CS31310"

    
