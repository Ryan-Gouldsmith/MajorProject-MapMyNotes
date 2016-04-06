from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.user import User
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from datetime import datetime
import mock
import os
from googleapiclient.http import HttpMock, HttpRequest


#https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good.
class TestIntegrationEditMetaData(LiveServerTestCase):


    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SECRET_KEY'] = 'Secret key'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")

        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = Oauth_Service()
        file_path = app.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        self.credentials_oauth = oauth_service.exchange_code(flow, "123code", http=http_mock)

        self.patch = mock.patch.object(SessionHelper, "check_if_session_contains_credentials")
        self.cred_mock = self.patch.start()
        self.cred_mock.return_value = True

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials_oauth.to_json()

        return app

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Title")
        note_meta_data.save()
        self.note_meta_data_id = note_meta_data.id

        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id


        self.note = Note(file_path, self.note_meta_data_id, self.user_id)
        self.note.save()
        self.create_app()

    def tearDown(self):
        self.driver.quit()
        mock.patch.stopall()

    def test_edit_form_is_displayed_on_the_page(self):
        self.driver.get(self.get_server_url() + "/metadata/edit/" + str(self.note.id))
        form = self.driver.find_element_by_class_name("edit_form")
        assert form.is_displayed() is True

    def test_edit_form_populates_existing_information_correctly(self):
        self.driver.get(self.get_server_url() + "/metadata/edit/" + str(self.note.id))

        module_code_field = self.driver.find_element_by_class_name('module_code').get_attribute("value")

        lecturer_field = self.driver.find_element_by_class_name('lecturer').get_attribute("value")

        location = self.driver.find_element_by_class_name('location').get_attribute("value")

        date = self.driver.find_element_by_class_name("date").get_attribute("value")
        time = self.driver.find_element_by_class_name("time").get_attribute('value')

        title = self.driver.find_element_by_class_name("title").get_attribute("value")

        assert module_code_field == 'CS31310'
        assert lecturer_field == "Mr Foo"
        assert location == "C11 Hugh Owen"
        assert date == "20 January 2016"
        assert time == "15:00"
        assert title == "Title"

    def test_ensure_the_fields_have_required_key(self):
        self.driver.get(self.get_server_url() + "/metadata/edit/" + str(self.note.id))
        module_code = self.driver.find_element_by_class_name("module_code").get_attribute('required')
        lecturer = self.driver.find_element_by_class_name("lecturer").get_attribute('required')
        location = self.driver.find_element_by_class_name("location").get_attribute('required')
        date = self.driver.find_element_by_class_name("date").get_attribute('required')
        title = self.driver.find_element_by_class_name('title').get_attribute('required')

        assert module_code == "true"
        assert lecturer == "true"
        assert location == "true"
        assert date == "true"
        assert title == "true"
