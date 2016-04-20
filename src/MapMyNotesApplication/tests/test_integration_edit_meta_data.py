import os
from datetime import datetime

import mock
from flask.ext.testing import LiveServerTestCase
from googleapiclient.http import HttpMock
from selenium import webdriver

from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User


# https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good.
class TestIntegrationEditMetaData(LiveServerTestCase):
    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SECRET_KEY'] = 'Secret key'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__), "mock-data/authorised_credentials.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")

        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = OauthService()
        file_path = app.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        self.credentials_oauth = oauth_service.exchange_code(flow, "123code", http=http_mock)

        cred_obj = oauth_service.create_credentials_from_json(self.credentials_oauth.to_json())
        auth = HttpMock(self.authorised_credentials, {'status': 200})
        self.oauth_return = oauth_service.authorise(auth, self.credentials_oauth.to_json())
        oauth_service.create_credentials_from_json(self.credentials_oauth.to_json())
        calendar_service = GoogleCalendarService()

        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
        service = calendar_service.build(http_mock)

        self.google_response = {"items": [
            {

                "kind": "calendar#event",
                "etag": "\"1234567891012345\"",
                "id": "ideventcalendaritem1",
                "status": "confirmed",
                "htmlLink": "https://www.google.com/calendar/event?testtest",
                "created": "2014-09-10T14:53:25.000Z",
                "updated": "2014-09-10T14:54:12.748Z",
                "summary": "CS31310",
                "description": "\"http://localhost:5000/show_note/1\"",
                "creator": {
                    "email": "test@gmail.com",
                    "displayName": "Tester",
                    "self": 'true'
                },
                "organizer": {
                    "email": "test@gmail.com",
                    "displayName": "Test",
                    "self": 'true'
                },
                "start": {
                    "dateTime": "2016-01-20T15:00:00Z"
                },
                "end": {
                    "dateTime": "2016-01-20T16:30:00Z"
                },
                "transparency": "transparent",
                "visibility": "private",
                "iCalUID": "123456789@google.com",
                "sequence": 0,
                "guestsCanInviteOthers": 'false',
                "guestsCanSeeOtherGuests": 'false',
                "reminders": {
                    "useDefault": 'true'
                }
            }
        ]
        }
        self.new_event = {"items": [
            {
                "kind": "calendar#event",
                "etag": "\"12334455667\"",
                "id": "123456789",
                "status": "confirmed",
                "htmlLink": "http://localhost/show_note/1",
                "created": "2016-03-24T08:59:46.000Z",
                "updated": "2016-03-27T22:42:07.278Z",
                "summary": "CS31310",
                "description": "\"http://localhost:5000/show_note/1\"",
                "creator": {
                    "email": "test@gmail.com",
                    "displayName": "Test",
                    "self": True
                },
                "organizer": {
                    "email": "test@gmail.com",
                    "displayName": "test",
                    "self": True
                },
                "start": {
                    "dateTime": "2016-01-20T13:00:00Z"
                },
                "end": {
                    "dateTime": "2016-01-20T14:30:00Z"
                },
                "iCalUID": "test124@google.com",
                "sequence": 0,
                "reminders": {
                    "useDefault": True
                }
            }
        ]
        }
        self.updated_response = {
            "kind": "calendar#event",
            "etag": "\"12334455667\"",
            "id": "123456789",
            "status": "confirmed",
            "htmlLink": "http://newupdatednote.co.uk/1",
            "created": "2016-03-24T08:59:46.000Z",
            "updated": "2016-03-27T22:42:07.278Z",
            "summary": "CS31310",
            "description": "\"http://localhost:5000/show_note/1\"",
            "creator": {
                "email": "test@gmail.com",
                "displayName": "Test",
                "self": True
            },
            "organizer": {
                "email": "test@gmail.com",
                "displayName": "test",
                "self": True
            },
            "start": {
                "dateTime": "2016-01-20T13:00:00Z"
            },
            "end": {
                "dateTime": "2016-01-20T14:30:00Z"
            },
            "iCalUID": "test124@google.com",
            "sequence": 0,
            "reminders": {
                "useDefault": True
            }
        }

        self.patch = mock.patch.object(SessionHelper, "check_if_session_contains_credentials")
        self.cred_mock = self.patch.start()
        self.cred_mock.return_value = True

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials_oauth.to_json()

        self.oauth_patch = mock.patch.object(OauthService, "authorise")
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.oauth_return

        self.google_patch = mock.patch.object(GoogleCalendarService, "execute_request")
        self.google_mock = self.google_patch.start()
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        self.google_mock.side_effect = [self.google_response, self.new_event, self.google_response, self.updated_response]

        self.credentials_patch = mock.patch.object(OauthService, 'get_credentials')
        self.credentials_mock = self.credentials_patch.start()
        self.credentials_mock.return_value = oauth_service.credentials

        self.user_patch = mock.patch.object(SessionHelper, 'return_user_id')
        self.user_mock = self.user_patch.start()
        self.user_mock.return_value = 1

        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640)
        file_path = "upload/test.png"
        module_code = ModuleCode('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20th January 2016 15:00", "%dth %B %Y %H:%M")
        note_meta_data = NoteMetaData("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Title")
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

    def test_when_editing_the_date_updates_event_link_should_be_new_html(self):
        self.driver.get(self.get_server_url() + "/metadata/edit/" + str(self.note.id))
        module_code = self.driver.find_element_by_class_name("module_code")
        module_code.clear()
        module_code.send_keys('CS31310')
        lecturer = self.driver.find_element_by_class_name("lecturer")
        lecturer.clear()
        lecturer.send_keys("Mr Foo")
        location = self.driver.find_element_by_class_name("location")
        location.clear()
        location.send_keys("C11 Hugh Owen")
        date = self.driver.find_element_by_class_name("date")
        date.clear()
        date.send_keys("20 January 2016")
        time = self.driver.find_element_by_class_name("time")
        time.clear()
        time.send_keys("15:00")
        title = self.driver.find_element_by_class_name('title')
        title.clear()
        title.send_keys("Title")
        submit = self.driver.find_element_by_class_name('submit')
        submit.click()
        print self.driver.page_source
        new_event_url = self.driver.find_element_by_class_name('calendar_link').get_attribute('href')

        assert new_event_url == "http://newupdatednote.co.uk/1"

    def test_when_editing_the_date_it_shows_unable_to_save_to_calendar_if_no_event_was_found(self):
        self.driver.get(self.get_server_url() + "/metadata/edit/" + str(self.note.id))
        module_code = self.driver.find_element_by_class_name("module_code")
        module_code.clear()
        module_code.send_keys('CS31310')
        lecturer = self.driver.find_element_by_class_name("lecturer")
        lecturer.clear()
        lecturer.send_keys("Mr Foo")
        location = self.driver.find_element_by_class_name("location")
        location.clear()
        location.send_keys("C11 Hugh Owen")
        date = self.driver.find_element_by_class_name("date")
        date.clear()
        date.send_keys("31 January 2016")
        time = self.driver.find_element_by_class_name("time")
        time.clear()
        time.send_keys("15:00")
        title = self.driver.find_element_by_class_name('title')
        title.clear()
        title.send_keys("Title")
        submit = self.driver.find_element_by_class_name('submit')
        submit.click()
        calendar_text = self.driver.find_element_by_class_name('saved_to_cal')

        assert calendar_text.text == "Unable to save to calendar"

