from flask import Flask
from flask.ext.testing import TestCase

from MapMyNotesApplication import database
from MapMyNotesApplication.models.input_validator import InputValidator


class TestInputValidator(TestCase):
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
        self.valid_credentials = {'module_code_data': "CS31310", "lecturer_name_data": "foo",
                                  "location_data": " a room", "title_data": "title", 'date_data': "12 March 2016",
                                  "time_data": "13:00"}

        self.invalid_length_credentials = {'module_code_data': "CS31310" * 100, "lecturer_name_data": "foo" * 100,
                                           "location_data": " a room", "title_data": "title",
                                           'date_data': "12 March 2016",
                                           "time_data": "13:00"}

        self.invalid_spaced_credentials = {'module_code_data': "  " * 100, "lecturer_name_data": "foo" * 100,
                                           "location_data": " a room", "title_data": "title",
                                           'date_data': "12 March 2016",
                                           "time_data": "13:00"}

        self.missing_credentials = {"lecturer_name_data": "foo" * 100,
                                    "location_data": " a room", "title_data": "title", 'date_data': "12 March 2016",
                                    "time_data": "13:00"}

    def test_get_errors_returns_empty_array_when_theres_no_errors(self):
        validator = InputValidator(self.valid_credentials)

        assert validator.get_errors() == []

    def test_check_all_params_are_less_than_schema_length_returns_true_when_data_is_valid(self):
        validator = InputValidator(self.valid_credentials)
        is_over_length = validator.check_all_params_are_less_than_schema_length()

        assert is_over_length is True

    def test_check_all_params_exist_for_valid_data_returns_true(self):
        validator = InputValidator(self.valid_credentials)
        all_exist = validator.check_all_params_exist()

        assert all_exist is True

    def test_check_all_params_are_less_than_schema_length_returns_false_when_data_is_valid(self):
        validator = InputValidator(self.invalid_length_credentials)
        is_over_length = validator.check_all_params_are_less_than_schema_length()

        assert is_over_length is False

    def test_check_all_params_exist_for_invalid_data_returns_false_if_theres_spaces(self):
        validator = InputValidator(self.invalid_spaced_credentials)
        all_exist = validator.check_all_params_exist()

        assert all_exist is False

    def test_test_check_all_params_exist_for_invalid_data_returns_false_if_theres_missing_values(self):
        validator = InputValidator(self.missing_credentials)
        all_exist = validator.check_all_params_exist()

        assert all_exist is False
