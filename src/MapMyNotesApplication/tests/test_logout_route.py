from MapMyNotesApplication import application, database
from flask import session
from flask.ext.testing import TestCase


class TestLogoutRoute(TestCase):
    def create_app(self):
        app = application
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_logout_route_returns_a_200_error(self):
        # session manipulation http://flask.pocoo.org/docs/0.10/testing/
        with self.client as client:
            with client.session_transaction() as session_value:
                session_value['credentials'] = "test credentials"

            response = client.get("/logout")
            assert response.status_code == 302

    def test_logout_route_does_not_permit_post_requests(self):
        # session manipulation http://flask.pocoo.org/docs/0.10/testing/
        with self.client as client:
            with client.session_transaction() as session_value:
                session_value['credentials'] = "test credentials"

            response = client.post("/logout")
            assert response.status_code == 405

    def test_logout_removes_the_credentials_key_from_session(self):
        # session manipulation http://flask.pocoo.org/docs/0.10/testing/
        with self.client as client:
            with client.session_transaction() as session_value:
                session_value['credentials'] = "test credentials"

            response = client.get("/logout")
            has_credentials_key = 'credentials' in session
            assert has_credentials_key is False

    def test_logout_removes_the_user_id_from_session(self):
        # session manipulation http://flask.pocoo.org/docs/0.10/testing/
        with self.client as client:
            with client.session_transaction() as session_value:
                session_value['credentials'] = "test credentials"
                session_value['user_id'] = 1

            response = client.get("/logout")
            has_user_key = 'user_id' in session
            assert has_user_key is False
