from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.user import User
from flask.ext.testing import TestCase


class TestIntegrationViewAllNotes(TestCase):
    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        user = User("Test@gmail.com")
        database.session.add(user)
        database.session.commit()
        with self.client.session_transaction() as session:
            session['user_id'] = user.id

    def test_show_all_notes_returns_200_success_code(self):
        response = self.client.get("/view_notes")

        assert response.status_code is 200

    def test_redirect_to_homepage_if_user_session_not_set(self):
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.get("/view_notes")

        location = response.headers.get("Location").split("http://localhost")
        assert location[1] == "/"
