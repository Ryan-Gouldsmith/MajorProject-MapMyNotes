from MapMyNotesApplication import application, database
import pytest
from MapMyNotesApplication.models.user import User
from sqlalchemy import func
from flask.ext.testing import TestCase
from flask import Flask


class TestUser(TestCase):

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

    def test_find_a_user_by_email_address_should_return_user(self):
        user = User("test@mail.co.uk")
        user.save()

        found_user = User.find_user_by_email_address("test@mail.co.uk")
        assert found_user.id == user.id

    def test_finding_a_user_by_email_address_which_doesnt_exist(self):
        found_user = User.find_user_by_email_address('nonexistant@test.co.uk')

        assert found_user is None
