from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.module_code import Module_Code
from datetime import datetime

#https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good.
class TestIntegrationEditMetaData(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
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

        self.note = Note(file_path,note_meta_data.id)
        self.note.save()

    def tearDown(self):
        self.driver.quit()

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

        title = self.driver.find_element_by_class_name("title").get_attribute("value")

        assert module_code_field == 'CS31310'
        assert lecturer_field == "Mr Foo"
        assert location == "C11 Hugh Owen"
        assert date == "20th January 2016 15:00"
        assert title == "Title"
