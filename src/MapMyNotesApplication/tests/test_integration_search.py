from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.user import User
from MapMyNotesApplication.models.session_helper import SessionHelper
import mock
from datetime import datetime


class TestIntegrationSearch(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'


        self.user_patch = mock.patch.object(SessionHelper, 'return_user_id')
        self.user_mock = self.user_patch.start()
        self.user_mock.return_value = 1

        self.user_in_session = mock.patch.object(SessionHelper,
        'is_user_id_in_session')
        self.user_in_session_mock = self.user_in_session.start()
        self.user_in_session_mock.return_value = True

        return app

    def setUp(self):
        # Ideas on how to create the driver and use it. https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/

        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )
        database.session.close()
        database.drop_all()
        database.create_all()
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()
        self.module_code_id = module_code.id

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "Dummy")
        note_meta_data.save()
        self.note_meta_data_id = note_meta_data.id

        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id

        user_two = User("newUser@gmail.com")
        database.session.add(user_two)
        database.session.commit()
        self.second_user_id = user_two.id

        note_meta_data_two = Note_Meta_Data("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "Second")
        note_meta_data_two.save()
        self.second_meta_data_id = note_meta_data_two.id


        note = Note('uploads/', self.note_meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()

        note_two = Note('other_users', self.second_meta_data_id, self.second_user_id)
        database.session.add(note_two)
        database.session.commit()

        self.create_app()

    def tearDown(self):
        self.driver.quit()
        mock.patch.stopall()

    def test_form_with_search_bar_is_displayed(self):
        self.driver.get(self.get_server_url() + "/search")
        form = self.driver.find_element_by_class_name("search_form")
        search_field = self.driver.find_element_by_class_name('search_field')

        assert form.is_displayed() is True
        assert search_field.is_displayed() is True

    def test_searching_for_form_returns_a_note(self):
        self.driver.get(self.get_server_url() + "/search")
        search_field = self.driver.find_element_by_class_name('search_field')
        search_field.send_keys("CS31310")
        submit = self.driver.find_element_by_class_name("submit").click()

        notes = self.driver.find_element_by_class_name("notes")
        print self.driver.page_source

        titles = self.driver.find_elements_by_class_name('note_title')
        expected_titles = []
        for title in titles:
            expected_titles.append(title.text)

        view_notes = self.driver.find_elements_by_class_name('view_notes')
        expected_view_notes = []
        for note in view_notes:
            expected_view_notes.append(note.text)

        assert notes.is_displayed() is True
        assert "Dummy" in expected_titles[0]
        assert 'View note' in expected_view_notes

    def test_searching_for_a_module_that_doesnt_exist_return_message(self):
        self.driver.get(self.get_server_url() + "/search")
        search_field = self.driver.find_element_by_class_name('search_field')
        search_field.send_keys("SE31520")
        submit = self.driver.find_element_by_class_name("submit").click()

        error_message = self.driver.find_element_by_class_name("message")

        assert error_message.text == "Sorry could not find any modules with that code"

    def test_clicking_view_note_shows_the_note_with_meta_data(self):
        self.driver.get(self.get_server_url() + "/search")
        search_field = self.driver.find_element_by_class_name('search_field')
        search_field.send_keys("CS31310")
        submit = self.driver.find_element_by_class_name("submit").click()
        view_notes = self.driver.find_elements_by_class_name('view_notes')

        view_notes[0].click()

        print self.driver.page_source

        assert "show_note/1" in self.driver.current_url

    def test_when_searched_for_it_shows_the_user_what_they_have_search(self):
        self.driver.get(self.get_server_url() + "/search")
        search_field = self.driver.find_element_by_class_name('search_field')
        search_field.send_keys("CS31310")
        submit = self.driver.find_element_by_class_name("submit").click()

        searched = self.driver.find_element_by_class_name("searched")

        assert "CS31310" in searched.text

    def test_only_display_the_logged_in_users_notes_not_others(self):
        self.driver.get(self.get_server_url() + "/search")
        search_field = self.driver.find_element_by_class_name('search_field')
        search_field.send_keys("CS31310")
        submit = self.driver.find_element_by_class_name("submit").click()

        titles = self.driver.find_elements_by_class_name('note_title')
        expected_titles = []
        for title in titles:
            expected_titles.append(title.text)

        assert "Second" not in expected_titles
