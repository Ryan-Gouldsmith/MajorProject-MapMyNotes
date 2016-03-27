from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from datetime import datetime
from flask.ext.testing import TestCase
from flask import Flask

class TestNoteMetaData(TestCase):

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

    def test_saving_a_lecturers_name_should_return_correct_name(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        #http://www.tutorialspoint.com/python/time_strptime.htm Help from hereda
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "Title")
        database.session.add(meta_data)
        database.session.commit()

        database_meta_data = Note_Meta_Data.query.first()

        assert database_meta_data.lecturer == meta_data.lecturer

    def test_the_save_function_in_note_meta_data(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "Title")
        meta_data.save()

        database_meta_data = Note_Meta_Data.query.first()

        assert database_meta_data.lecturer == meta_data.lecturer

    def test_a_name_which_is_too_long_should_return_false(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        too_long_lecturers_name = "a" * 110
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data(too_long_lecturers_name, module_code.id, "C11 Hugh Owen", date, "Title")
        result = meta_data.save()
        assert False is result

    def test_a_name_which_is_fine_for_length_should_return_true(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        lecturer_name = "Dr Mark Foobar"
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data(lecturer_name, module_code.id, "C11 Hugh Owen", date, "Title")

        result = meta_data.save()

        assert True is result

    def test_it_saves_a_meta_data_note_and_returns_correct_id(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")
        meta_data.save()

        expected_id = 1

        assert meta_data.id == expected_id

    def test_saves_a_module_code_as_part_of_a_foreign_key(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "Title")

        meta_data.save()

        assert meta_data.module_code.module_code == "CS31310"

    def test_the_location_meta_data_returns_the_correct_value(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")

        meta_data.save()

        assert meta_data.location == "C11 Hugh Owen"

    def test_that_location_cant_be_over_100_characters(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        location = "Seat" * 40

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, location,date, 'Title')

        result = meta_data.save()

        assert result is False

    def test_the_date_returned_is_the_correct_date(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        location = "Seat" * 40

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, location,date, "title")

        result = meta_data.save()

        assert meta_data.date.strftime("%dth %B %Y %H:%M") == "20th January 2016 15:00"

    def test_find_existing_meta_data_should_return_that_instance(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")

        result = meta_data.save()

        found_example = Note_Meta_Data.find_meta_data(meta_data)

        assert type(found_example) is Note_Meta_Data

        assert found_example == meta_data

    def test_find_exisitig_meta_data_should_return_none_bad_data(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")

        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")

        result = meta_data.save()

        bad_meta_data = Note_Meta_Data("Dr Bad", module_code.id, "C11 Hugh Owen", date, 'A Title')

        found_example = Note_Meta_Data.find_meta_data(bad_meta_data)

        assert found_example is None

    def test_saving_a_new_module_code_updates_current_object_module_code(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")
        result = meta_data.save()

        module_code_new = Module_Code("SE31520")
        module_code_new.save()

        meta_data.update_module_code_id(module_code_new.id)

        assert meta_data.module_code_id == 2
        assert meta_data.module_code.module_code == "SE31520"

    def test_saving_title_with_meta_data_returns_the_correct_title(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        meta_data = Note_Meta_Data("Dr Test", module_code.id, "C11 Hugh Owen", date, "title")
        result = meta_data.save()

        assert meta_data.title == "title"
