from MapMyNotesApplication import application, database
import pytest
from flask import Flask
from MapMyNotesApplication.models.session_helper import SessionHelper
from flask.ext.testing import TestCase


class TestSessionHelper(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        """
         http://blog.toast38coza.me/adding-a-database-to-a-flask-app/
         Used to help with the test database, could move this to a config file.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['SECRET_KEY'] = "secret"
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_session_in_credentials_returns_false_when_no_key(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session.clear()

        credentials = session_helper.check_if_session_contains_credentials(session)
        assert credentials is False

    def test_session_in_credentials_returns_true_when_theres_a_key(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session.clear()
            session = {"credentials": "Test credentials"}

        assert session_helper.check_if_session_contains_credentials(session) is True

    def test_returns_the_correct_credentials_from_the_session(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session = {"credentials": "Test credentials"}

        assert "Test credentials" in session_helper.return_session_credentials(session)

    def test_returns_the_correct_user_id_from_session(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session = {"user_id": 6}
        assert session_helper.return_user_id(session) is 6

    def test_is_user_id_in_session_returns_true(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session = {"user_id": 1}

        assert session_helper.is_user_id_in_session(session) is True

    def test_is_user_id_in_session_returns_false(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session.clear()

        assert session_helper.is_user_id_in_session(session) is False

    def test_errors_in_session_returns_true(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session['errors'] = 'errors!'

        assert session_helper.errors_in_session(session) is True

    def test_errors_in_session_returns_false(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session.clear()

        assert session_helper.errors_in_session(session) is False

    def test_get_errors_returns_correct_errors(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session['errors'] = 'errors!'

        assert session_helper.get_errors(session) == "errors!"

    def test_delete_session_errors_removes_them_properly(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session['errors'] = 'errors!'

        session_helper.delete_session_errors(session)
        in_session = 'errors' in session
        assert in_session is False

    def test_setting_errors_in_session_successfully_sets_session(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session_helper.set_errors_in_session(session, "test")

        errors_value = session['errors']
        assert errors_value == "test"

    def test_setting_user_id_in_session_successfully_sets_key(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session_helper.save_user_id_to_session(session, 4)

        user_id = session['user_id']
        assert user_id is 4

    def test_deleting_credentials_from_session_removes_them(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session['credentials'] = "credentials"

        session_helper.delete_credentials_from_session(session)
        credentials_in_session = 'credentials' in session
        assert credentials_in_session is False

    def test_deleting_user_id_from_session_removes_it(self):
        session_helper = SessionHelper()
        with self.client.session_transaction() as session:
            session['user_id'] = 1

        session_helper.delete_user_from_session(session)
        user_in_session = 'user_id' in session
        assert user_in_session is False
