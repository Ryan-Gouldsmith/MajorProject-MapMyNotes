from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium.webdriver.common.keys import Keys

from MapMyNotesApplication.models.note import Note
from sqlalchemy import func
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from datetime import datetime


class TestIntegretationShowNote(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        # Ideas on how to create the driver and use it. https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_to_view_all_notes(self):
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date)
        note_meta_data.save()

        note = Note('uploads/', note_meta_data.id)
        database.session.add(note)
        database.session.commit()

        self.driver.get(self.get_server_url() + "/view_notes")
        notes = self.driver.find_elements_by_class_name("notes")
        note_module = self.driver.find_elements_by_class_name("note_module")
        module_codes = []
        for module in note_module:
            module_codes.append(module.text)

        note_module_link = self.driver.find_elements_by_class_name("note_link")
        note_links = []
        for link in note_module_link:
            note_links.append(link.get_attribute("href").split("http://localhost:5000")[1])

        note_lecturers = self.driver.find_elements_by_class_name("lecturer")
        lecturers = []
        for lecturer in note_lecturers:
            lecturers.append(lecturer.text)

        assert len(notes) is 1
        assert "CS31310" in module_codes
        assert "/show_note/1" in note_links
        assert "By Mr Foo" in lecturers
