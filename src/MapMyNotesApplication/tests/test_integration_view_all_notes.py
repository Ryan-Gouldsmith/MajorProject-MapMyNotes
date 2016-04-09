from datetime import datetime

import mock
from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver


class TestIntegretationShowNote(LiveServerTestCase):
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
        self.driver.set_window_size(1024, 640)
        database.session.close()
        database.drop_all()
        database.create_all()

        module_code = ModuleCode('CS31310')
        database.session.add(module_code)
        database.session.commit()
        self.module_code_id = module_code.id

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = NoteMetaData("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "Some title")
        note_meta_data.save()
        self.note_meta_data_id = note_meta_data.id

        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id

        note = Note('uploads/', self.note_meta_data_id, self.user_id)
        database.session.add(note)
        database.session.commit()
        self.create_app()

    def tearDown(self):
        self.driver.quit()
        mock.patch.stopall()

    def test_to_view_all_notes(self):

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

        note_titles = self.driver.find_elements_by_class_name("title")
        titles = []
        for title in note_titles:
            titles.append(title.text)
        assert len(notes) is 1
        assert "CS31310" in module_codes
        assert "/show_note/1" in note_links
        assert "By Mr Foo" in lecturers
        assert "Some title" in titles
