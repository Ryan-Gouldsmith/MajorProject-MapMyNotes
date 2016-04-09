from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.user import User
from flask.ext.testing import TestCase


class TestSearchRoute(TestCase):
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

    def test_search_route_with_code_returns_200_status_code(self):
        response = self.client.get("/search?module_code=CS31310")

        assert response.status_code == 200

    def test_search_route__with_code_can_not_permit_post_requests(self):
        response = self.client.post("/search?module_code=CS31310")
        assert response.status_code == 405

    def test_search_route_returns_200_status_code(self):
        response = self.client.get('/search')
        assert response.status_code == 200

    def test_search_with_post_request_returns_405(self):
        response = self.client.post("/search")
        assert response.status_code == 405

    def test_if_user_not_in_session_return_to_homepage(self):
        with self.client.session_transaction() as session:
            session.clear()

        response = self.client.get('/search')
        location = response.headers.get('Location').split("http://localhost")

        assert location[1] is "/"
