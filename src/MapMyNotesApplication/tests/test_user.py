from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.user import User
from sqlalchemy import func

class TestUser(object):
    def setup(self):
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.app = application.test_client()
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_creating_a_new_user_should_return_1_as_id(self):
        user = User("test@mail.co.uk")
        database.session.add(user)
        database.session.commit()

        assert user.id == 1

    def test_creating_a_user_should_return_the_correct_email(self):
        user = User("test@mail.co.uk")
        database.session.add(user)
        database.session.commit()

        find_user = User.query.first()
        assert find_user.email_address == 'test@mail.co.uk'

    def test_user_function_to_save_a_user_successfull(self):
        user = User("test@mail.co.uk")
        user.save()

        find_user = User.query.first()

        assert find_user.id == 1
        assert find_user.email_address == "test@mail.co.uk"
