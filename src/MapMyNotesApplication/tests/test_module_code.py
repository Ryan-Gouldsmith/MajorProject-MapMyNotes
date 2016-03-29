from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from flask.ext.testing import TestCase
from flask import Flask


class TestNote(TestCase):

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

    def test_saving_a_module_code(self):
        module_code = Module_Code("CS31310")
        database.session.add(module_code)
        database.session.commit()
        assert module_code.id == 1

    def test_saving_module_code_getting_module_back(self):
        module_code = Module_Code("CS31310")
        database.session.add(module_code)
        database.session.commit()
        assert module_code.module_code == "CS31310"

    def test_the_save_function(self):
        module_code = Module_Code("CS31310")
        module_code.save()
        assert module_code.module_code == "CS31310"

        assert module_code.id == 1

    def test_static_function_returning_same_module_code(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        module_code_obj = Module_Code.find_id_by_module_code("CS31310")

        assert module_code.id == module_code_obj.id

    def test_static_function_returns_none_if_not_found(self):
        module_code = Module_Code("CS31310")
        module_code.save()

        module_code_obj = Module_Code.find_id_by_module_code("SE31520")

        assert None is module_code_obj
