from MapMyNotesApplication import application, database
import pytest
from flask import Flask
from MapMyNotesApplication.models.session_helper import SessionHelper
from flask.ext.testing import TestCase

class TestSessionHelper(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
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
            assert session_helper.check_if_session_contains_credentials(session) is False

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
